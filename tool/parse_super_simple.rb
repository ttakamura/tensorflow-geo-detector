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
    if n.text && n.text().size > 1
      text = normalize(n.text()).gsub(/[\n\s\t]*/,'')

      if text =~ name_pattern
        # raise "#{text} name"
        block.call n, text, 1
      elsif text =~ addr_pattern
        # raise "#{text} addr"
        block.call n, text, 2
      elsif n.children.size == 0
        block.call n, text, 0
      else
        traverse(n, name_pattern, addr_pattern, &block)
      end
    end
  end
end

def convert file_path, name_pattern, addr_pattern
  parse(file_path, name_pattern, addr_pattern) do |node, text, category|
    if category != 0 || node.text?
      if text.size > 1 && !(text =~ /\A[0-9]+\z/)
        # puts [text, category, node.path].join("\t")
        puts [text, category].join("\t")
      end
    end
  end
end

def ngram_regexp text, ngram
  # tokens = normalize(text).split(//).map{ |c| Regexp.escape(c) }
  # tokens = tokens.each_cons(ngram).map{ |b| b.join("") }
  regexp = /\A(#{ text })+\z/
  regexp
end

def normalize text
  LocalPlaceNormalizer.normalize_hoge text
end

html_file   = ARGV.shift
name_regexp = ngram_regexp('にくや萬野', 3)
addr_regexp = ngram_regexp('大阪府大阪市北区曽根崎2-10-9', 3)

convert(html_file, name_regexp, addr_regexp)
