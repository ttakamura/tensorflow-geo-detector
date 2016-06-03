# coding: utf-8
#
# tools02 サーバなどで実行する
#
CSV.open('/tmp/item_places.csv', 'w') do |csv|
  Item.original.joins(:place).includes(:place).find_each do |i|
    if i.link_url.present? && i.place
      csv.puts [i.id, i.link_url, i.place.name, i.place.address]
    end
  end
end
