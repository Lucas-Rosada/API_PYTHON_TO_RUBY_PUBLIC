require 'sinatra'
require 'net/http'
require 'json'
require 'uri'

# Configuração da porta
set :port, 4567

get '/' do
  @data = fetch_data_from_api
  erb :index
end

# Função que busca dados
def fetch_data_from_api
  url = URI.parse('http://localhost:5000/data')  
  response = Net::HTTP.get_response(url)

  if response.is_a?(Net::HTTPSuccess)
    JSON.parse(response.body)
  else
    [] 
  end
end

if __FILE__ == $0

  Sinatra::Application.run!
end
