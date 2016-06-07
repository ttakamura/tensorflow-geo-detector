# coding: utf-8
require 'csv'
#
# tabelog_only から tabelog_final を生成する
# 名前と住所が上手く HTML にヒットしなかったものを取り除く
#

def cleanup_row row, out_csv
  hash = row[2]
  open("tabelog_only/docs/#{hash}","r") do |file|
    body = file.read
    if (body =~ /\t1$/) && (body =~ /\t2$/)
      open("tabelog_final/docs/#{hash}","w") do |out_html_file|
        out_html_file.write body
      end
      out_csv << row
    end
  end
end

CSV.open("tabelog_final/data.csv", "w") do |out_csv|
  CSV.open(ARGV.shift, "r").each do |row|
    cleanup_row row, out_csv
  end
end
