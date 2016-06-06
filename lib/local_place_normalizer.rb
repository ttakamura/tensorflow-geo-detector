# coding: utf-8

require 'csv'

class LocalPlaceNormalizer
  class << self
    def normalize_basic name
      LocalPlaceNormalizer.new.normalize_basic name
    end

    def normalize_name name
      LocalPlaceNormalizer.new.normalize_name name
    end

    def normalize_address address
      LocalPlaceNormalizer.new.normalize_address address
    end

    # CSVファイルをコンバートする。（テスト用）
    # CSVファイルの最初のカラムの値を使います。
    # 例:
    #   ruby -r "./misc/local_place_normalizer.rb" -e "LocalPlaceNormalizer.normalize_csv :address, '/home/tabdev/tab_places_all_address_20160328.csv'" | tee tab_places_result.txt
    #
    def normalize_csv type, path
      CSV.foreach(path, headers: true) do |row|
        value = row[0]
        puts "#{send("normalize_#{type}", value)} <<< #{value}" if value != nil
      end
    end
  end

  def normalize_basic name
    funcs = [
      :remove_whitespaces,
      :full_to_half,
      :kansuuji,
      :separator,
      :remove_ignore_symbol
    ]
    funcs.each do |func|
      name = send(func, name)
    end
    name
  end

  def normalize_name name
    funcs = [
      :remove_place_name,
      :remove_whitespaces,
      :full_to_half,
      :kansuuji,
      :separator,
      :remove_ignore_symbol,
      :remove_parenthesis,
    ]
    funcs.each do |func|
      name = send(func, name)
    end
    name
  end

  # normalize an address string
  def normalize_address address
    funcs = [
      :remove_whitespaces,
      :full_to_half,
      :kansuuji,
      :separator,
      :remove_ignore_symbol,
      :remove_parenthesis,
      :remove_japan_prefix,
      :remove_zip_code,
      :remove_choume,
      :normalize_floor,
      :remove_building_name,
      :remove_nearly
    ]
    funcs.each do |func|
      address = send(func, address)
    end
    address
  end

  # "赤から鍋 新宿駅前店" などの "地名+店" を削除する
  def remove_place_name str
    separator = '　\s\t」／…〜~'
    str.gsub /([^#{separator}])[#{separator}]+[^#{separator}]+(店|ビル)/, '\1'
  end

  def remove_whitespaces str
    str.gsub /[\s\t　]/, ''
  end

  def full_to_half str
    str = str.tr '０-９ａ-ｚＡ-Ｚ', '0-9a-zA-Z'
    str = str.tr '／＆？！',        '/&?!'
    str = str.upcase
  end

  def kansuuji str
    str.tr '一二三四五六七八九', '123456789'
  end

  def separator str
    str.gsub /[〜~ー－―−‐]/, '-'
  end

  def remove_parenthesis str
    begin_symbols = '[（\(【]'
    end_symbols   = '[）\)】]'
    str.gsub /#{begin_symbols}.+?#{end_symbols}/, ''
  end

  def remove_ignore_symbol str
    str.gsub /[・\?!]/, ''
  end

  def remove_japan_prefix str
    str.gsub /^日本,?/, ''
  end

  def remove_zip_code str
    str.gsub /^〒?\d+-\d+/, ''
  end

  def remove_choume str
    str = str.gsub /(\d+)丁目?(\d+)/, '\1-\2'  # 3丁目3番
    str = str.gsub /(\d+)丁目?/, '\1'          # 4丁目
    str = str.gsub /(\d+)番地?(\d+)/, '\1-\2'  # 2番3...  2番地3...
    str = str.gsub /(\d-\d+)番地?/, '\1'       # 1丁目4番(地)
    str = str.gsub /(\d+)号/, '\1'             # 5号
    str = str.gsub /(\d+)番地?/, '\1'          # 5番地
  end

  def normalize_floor str
    str = str.gsub /(\d+)(?:階)/, '\1F'
    str = str.gsub /地下(\d+)F/, 'B\1F'
  end

  def remove_building_name str
    str.gsub /(\d+(\-\d+)+)[^\d\-].+\Z/, '\1'
  end

  def remove_nearly str
    str.gsub /周辺\Z/, ''
  end
end
