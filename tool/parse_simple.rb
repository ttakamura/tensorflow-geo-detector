# coding: utf-8
#
# とりあえず HTML を単純な文字列に変換する
#
require 'nokogiri'

JAP_REGEXP = /(?:\p{Hiragana}|\p{Katakana}|[ー－]|[一-龠々]|[0-9])+/

def parse file_path, &block
  doc = open(file_path, 'r') do |f|
    Nokogiri::HTML.parse(f.read)
  end
  doc.search('//text()').each do |node|
    blank_line = node.text =~ /^[\n\s｜\|]+$/
    html_line  = node.text =~ /<.+>/
    code_line  = node.text =~ /<!--/
    jap_line   = node.text =~ JAP_REGEXP
    if blank_line || html_line || code_line || (!jap_line)
      # nop
    else
      block.call node
    end
  end
end

def convert file_path, name_pattern, addr_pattern
  parse(file_path) do |node|
    if node.text =~ name_pattern
      print_with_annotate(node.text, '1')
    elsif node.text =~ addr_pattern
      print_with_annotate(node.text, '2')
    else
      print_with_annotate(node.text, '0')
    end
  end
end

def print_with_annotate text, category
  text = text.gsub(/[\n\t\s]/, '')
  puts [category, text].join("\t")
end

def trigram_regexp text

end

def normalize text
  text.tr("０-９", "0-9")
end

html_file   = ARGV.shift
name_regexp = trigram_regexp('にくや萬野')
addr_regexp = trigram_regexp('〒530-0057 大阪府大阪市北区曾根崎２丁目１０−９ 530 0057 丁目')

convert(html_file, name_regexp, addr_regexp)
