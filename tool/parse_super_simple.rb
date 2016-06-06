# coding: utf-8
#
# とりあえず HTML を分割する
#
require 'nokogiri'
require './lib/local_place_normalizer.rb'
require 'pry'

JAP_REGEXP = /(?:\p{Hiragana}|\p{Katakana}|[ー－]|[一-龠々]|[0-9])+/

def parse file_path, name_pattern, addr_pattern, &block
  doc = open(file_path, 'r') do |f|
    Nokogiri::HTML.parse(f.read)
  end
  traverse(doc, name_pattern, addr_pattern, &block)
  return true
  #
  # doc.search('//text()').each do |node|
  #   blank_line = node.text =~ /^[\n\s｜\|]+$/
  #   html_line  = node.text =~ /<.+>/
  #   code_line  = node.text =~ /<!--/
  #   num_line   = node.text =~ /^[0-9\n]+$/
  #   jap_line   = node.text =~ JAP_REGEXP
  #   if blank_line || html_line || code_line || num_line || (!jap_line)
  #     # nop
  #   else
  #     block.call node
  #   end
  # end
end

def traverse node, name_pattern, addr_pattern, &block
  node.children.each do |n|
    if n.text && n.text.size > 1
      text = n.text.gsub(/\n\s/,'')

      path = '/html/body/div[13]/div/div/div[3]/div[1]/div[9]/div[2]/table[1]/tbody/tr[4]/th/'
      if node.path == path
        p node
        raise 'Found!!'
      end

      if text =~ name_pattern
        block.call n, 1
      elsif text =~ addr_pattern
        block.call n, 2
      elsif n.children.size == 0
        block.call n, 0
      else
        traverse(n, name_pattern, addr_pattern, &block)
      end
    end
  end
end

def convert file_path, name_pattern, addr_pattern
  parse(file_path, name_pattern, addr_pattern) do |node, category|
    if node.text?
      # Nokogiri::CSS.xpath_for node.css_path
      # p node.css_path
      text = normalize(node.text).gsub(/[\n\t\s]/, '')
      if text.size > 1
        puts [text, category, node.path].join("\t")
      end
    end
  end
end

def annotate token, name_pattern, addr_pattern
  if token =~ name_pattern
    print_with_annotate(token, '1')
  elsif token =~ addr_pattern
    print_with_annotate(token, '2')
  else
    print_with_annotate(token, '0')
  end
end

def print_with_annotate token, category
  puts [category, token].join("\t")
end

def ngram_regexp text, ngram
  tokens = normalize(text).split(//).map{ |c| Regexp.escape(c) }
  tokens = tokens.each_cons(ngram).map{ |b| b.join("") }
  regexp = /^(#{ tokens.join("|") })+$/
  p regexp
  regexp
end

def normalize text
  LocalPlaceNormalizer.normalize_hoge text
end

html_file   = ARGV.shift
name_regexp = ngram_regexp('にくや萬野', 3)
addr_regexp = ngram_regexp('大阪府大阪市北区曽根崎2-10-9', 3)

convert(html_file, name_regexp, addr_regexp)
