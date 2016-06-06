# coding: utf-8
#
# とりあえず HTML を単純な文字列に変換する
#
require 'nokogiri'
require './lib/local_place_normalizer.rb'
require 'pry'

JAP_REGEXP = /(?:\p{Hiragana}|\p{Katakana}|[ー－]|[一-龠々]|[0-9])+/

def parse file_path, &block
  doc = open(file_path, 'r') do |f|
    Nokogiri::HTML.parse(f.read)
  end
  doc.search('//text()').each do |node|
    blank_line = node.text =~ /^[\n\s｜\|]+$/
    html_line  = node.text =~ /<.+>/
    code_line  = node.text =~ /<!--/
    num_line   = node.text =~ /^[0-9\n]+$/
    jap_line   = node.text =~ JAP_REGEXP
    if blank_line || html_line || code_line || num_line || (!jap_line)
      # nop
    else
      block.call node
    end
  end
end

def convert file_path, name_pattern, addr_pattern
  parse(file_path) do |node|
    text = normalize(node.text).gsub(/[\n\t\s]/, '')
    if text.size > 1
      if text =~ name_pattern
        print_with_annotate(node, '1')
      elsif text =~ addr_pattern
        print_with_annotate(node, '2')
      else
        print_with_annotate(node, '0')
      end
    end
  end
end

def print_with_annotate node, category
  # Nokogiri::CSS.xpath_for node.css_path
  p node.css_path
  puts [category, node.text].join("\t")
end

def trigram_regexp text
  x = normalize(text)
  x = Regexp.new("^(" + x.split(//).map{ |c| Regexp.escape(c) }.join("|") + ")+$")
  x
end

def normalize text
  LocalPlaceNormalizer.normalize_hoge text
end

html_file   = ARGV.shift
name_regexp = trigram_regexp('にくや萬野')
addr_regexp = trigram_regexp('〒530-0057 大阪府大阪市北区曾根崎２丁目１０−９ 530 0057 丁目')

convert(html_file, name_regexp, addr_regexp)
