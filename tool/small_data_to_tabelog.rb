require 'csv'
require './tool/parse_super_simple.rb'

def parse_id_map file
  hash = {}
  open(file, 'r').each_line do |line|
    a,b = line.chomp.split("\t")
    hash[a] = b
  end
  hash
end

@url_to_id = parse_id_map('small_data/url_id_map')

def convert_csv id, url, name, addr, source_row, out_csv
  hash = @url_to_id[url]
  if hash
    out_csv << [id, url, hash, name, addr]
    open("tabelog_only/docs/#{hash}", "w") do |doc_file|
      name_pattern = ngram_regexp(name)
      addr_pattern = ngram_regexp(addr)
      convert_html(doc_file, "small_data/html/#{hash}", name_pattern, addr_pattern)
    end
  end
end

CSV.open("tabelog_only/data.csv", "w") do |tabelog_data_csv|
  CSV.open("small_data/data.csv", "r").each do |row|
    id, url, name, addr = row
    if url =~ /tabelog\.com/
      convert_csv(id, url, name, addr, row, tabelog_data_csv)
    end
  end
end
