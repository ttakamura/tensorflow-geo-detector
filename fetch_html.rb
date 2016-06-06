# coding: utf-8
require 'net/http'
require 'uri'
require 'digest/md5'
require 'thread'

OUTPUT_DIR = 'data/html/'

INPUT_FILE  = open(ARGV.shift, 'r')
OUTPUT_FILE = open(ARGV.shift, 'w')
OUTPUT_Q = Queue.new

def crawl thread_id, url
  name = Digest::MD5.hexdigest(url.to_s)
  cache_file = "#{OUTPUT_DIR}/#{name}"

  if File.exist?(cache_file)
    puts "T#{thread_id} - Cached ... #{url} => #{name}"
    OUTPUT_Q.push [url.to_s, name].join("\t")
    return
  end

  puts "T#{thread_id} - Fetch ... #{url} => #{name}"

  Net::HTTP.start(url.host, url.port) do |http|
    res = http.get(url.path)
    if res.code == '200'
      open(cache_file, "w") do |file|
        file.write res.body
      end
      OUTPUT_Q.push [url.to_s, name].join("\t")
    else
      puts "HTTP Error #{res.code} #{url}"
    end
  end

  sleep(1) # 一応１秒スリープ
rescue => e
  puts e.inspect
end

def boot_threads thread_num, queue
  thread_num.times.map do |i|
    Thread.start do
      loop do
        url = queue[i].pop
        crawl(i, url)
      end
    end
  end
end

thread_num  = 1000
host_tables = {}
queue       = thread_num.times.map{ Queue.new }
threads     = boot_threads(thread_num, queue)

while line = INPUT_FILE.gets
  begin
    line = line.chomp
    url = URI.parse(line)
    host_tables[url.host] ||= (host_tables.size % thread_num)
    queue[host_tables[url.host]].push url
  rescue URI::InvalidURIError => e
    # p e
  end
end

until queue.all?(&:empty?)
  until OUTPUT_Q.empty?
    output_log = OUTPUT_Q.pop
    OUTPUT_FILE.puts output_log
  end
  sleep 10
end

threads.each{ |t| t.join }

INPUT_FILE.close
OUTPUT_FILE.close
