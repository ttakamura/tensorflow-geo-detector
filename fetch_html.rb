# coding: utf-8
require 'net/http'
require 'uri'
require 'digest/md5'
require 'thread'

OUTPUT_DIR = 'data/html/'

def crawl url
  name = Digest::MD5.hexdigest(url.path)
  cache_file = "#{OUTPUT_DIR}/#{name}"
  return if File.exist?(cache_file)

  # puts "Fetch ... #{url}"

  Net::HTTP.start(url.host, url.port) do |http|
    res = http.get(url.path)
    if res.code == '200'
      open(cache_file, "w") do |file|
        file.write res.body
      end
    end
  end

  sleep(1) # 一応１秒スリープ
end

thread_num  = 10
host_tables = {}

queue = thread_num.times.map{ Queue.new }

threads = thread_num.times.map do |i|
  Thread.start do
    loop do
      url = queue[i].pop
      crawl(url)
    end
  end
end

while line = gets
  begin
    url = URI.parse(line.chomp)
    host_tables[url.host] ||= (host_tables.size % thread_num)
    queue[host_tables[url.host]].push url
  rescue URI::InvalidURIError => e
    # Invalid URI
  end
end

until queue.all?(&:empty?)
  printf("\033[2J")
  queue.each_with_index do |q, i|
    puts "#{i} : " + ('*' * (q.size / 100))
  end
  sleep 1
end

threads.each{ |t| t.join }
