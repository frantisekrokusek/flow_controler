# Master Record class
class Record
  attr_reader :id
  def initialize(attributes = {})
    @id = attributes[:id]
    attributes.each do |key, value|
      if value.nil?
        instance_variable_set("@#{key}", 0)
      else
        instance_variable_set("@#{key}", value)
      end
      self.class.send(:attr_accessor, key)
    end
  end

  def key_array(array)
    # create keys
    keys_array = []
    array.reject! { |variable| variable == :@id }.each do |var|
      keys_array << var.to_s.delete_prefix('@').to_s
    end
    keys_array
  end

  def values_string(array)
    # create values
    values_array = array.map { |var| instance_variable_get var }
    values_array.map! { |value| value.class == String ? "'#{value}'" : value }
    values_array.map! { |value| value.nil? ? "nil" : value }
    values_array
  end

  def table
    self.class.to_s.downcase + "s"
  end

  def save
    array = instance_variables
    if id.nil?
      DB.execute("INSERT INTO #{table} (#{key_array(array).join(', ')}) VALUES (#{values_string(array).join(', ')})")
      @id = DB.last_insert_row_id
    else
      an_array = []
      key_array(array).each_with_index { |key, index| an_array << "#{key} = #{values_string(array)[index]}" }
      DB.execute("UPDATE #{table} SET #{an_array.join(', ')} WHERE id = ?", @id)
    end
  end

  def destroy
    # TODO: destroy the current instance from the database
    DB.execute("DELETE FROM #{table} WHERE id = ?", @id)
  end

  def self.find(id)
    DB.results_as_hash = true
    table = to_s.downcase + "s"
    results = DB.execute("SELECT * FROM #{table} WHERE id = ?", id).first
    if results
      attributes = (results.to_h.map { |key, value| [key.to_sym, value] }).to_h
      new(attributes)
    end
  end

  def self.all
    DB.results_as_hash = true
    table = to_s.downcase + "s"
    array = []
    result = DB.execute("SELECT * FROM #{table}")
    result.each do |item|
      attributes = (item.to_h.map { |key, value| [key.to_sym, value] }).to_h
      array << new(attributes)
    end
    array
  end
end
