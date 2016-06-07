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
end

def traverse node, name_pattern, addr_pattern, &block
  node.children.each do |n|
    block.call n, "", 0
    if n.text() && n.text().size > 1
      text = normalize(n.text()).gsub(/[\n\s\t]*/,'')
      if text =~ name_pattern
        block.call n, text, 1
      elsif text =~ addr_pattern
        block.call n, text, 2
      elsif n.children.size == 0
        block.call n, text, 0
      else
        traverse(n, name_pattern, addr_pattern, &block)
      end
    else
      traverse(n, name_pattern, addr_pattern, &block)
    end
  end
end

def convert_html io, file_path, name_pattern, addr_pattern
  parse(file_path, name_pattern, addr_pattern) do |node, text, category|
    if category != 0
      output_each_char io, text, category
    elsif node.text?
      output_each_char io, text, 0
    else
      output io, "<#{node.name}>", 0
    end
  end
end

def output io, text, category
  if text.size > 0
    io.puts [text, category].join("\t")
  end
end

def output_each_char io, text, category
  text.split(//).each do |c|
    io.puts [c, category].join("\t")
  end
end

def ngram_regexp text, ngram=0
  if ngram > 0
    tokens = normalize(text).split(//).map{ |c| Regexp.escape(c) }
    tokens = tokens.each_cons(ngram).map{ |b| b.join("") }
    /\A(#{ tokens.join("|") })+\z/
  else
    tokens = normalize(text)
    /\A(#{ tokens })+\z/
  end
end

def normalize text
  if text =~ /({\d}+)丁目({\d}+)番({\d}+)号/
    text = text.gsub(/(丁目|番|号)/, '-')
  end
  LocalPlaceNormalizer.normalize_hoge(text)
end

if __FILE__ == $0
  # サンプルコード
  html_file   = 'small_data/html/72374f695a840f98b24ad5c95d037359'
  name_regexp = ngram_regexp('')
  addr_regexp = ngram_regexp('', 3)
  convert_html(STDOUT, html_file, name_regexp, addr_regexp)
end
