require 'csv'

def convert id, url, name, addr, source_row, out_csv
  hash = @url_to_id[url]
  if hash
    if File.exist?("./small_data/html/#{hash}")
      out_csv << [id, url, hash, name, addr]
    end
  end
end

def parse_id_map file
  hash = {}
  open(file, 'r').each_line do |line|
    a,b = line.chomp.split("\t")
    hash[a] = b
  end
  hash
end

@url_to_id = parse_id_map('small_data/url_id_map')

CSV.open("tabelog_only/data.csv", "w") do |tabelog_data_csv|
  CSV.open("small_data/data.csv", "r").each do |row|
    id, url, name, addr = row
    if url =~ /tabelog\.com/
      convert(id, url, name, addr, row, tabelog_data_csv)
    end
  end
end
