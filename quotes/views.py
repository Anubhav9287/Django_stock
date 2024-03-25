from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

#pk_b73b3bde6c0f4bd5aeeee63749e2fb3f

def home(request):
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get("https://api.iex.cloud/v1/data/core/quote/" + ticker + "?token=pk_b73b3bde6c0f4bd5aeeee63749e2fb3f")
		try:
			api = json.loads(api_request.content)
			if api[0] == None:
				api = "Error...."
		except Exception as e:
			api = "Error...."
		return render(request,'home.html',{'api' : api })
	else:
		return render(request,'home.html',{'ticker' : "Enter a vaid symbol above.." })


def about(request):
	return render(request,'about.html',{})

def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added sucessfully!"))
			return redirect('add_stock')
		else:
			return redirect('add_stock')
	else:
		ticker = Stock.objects.all()
		output = []
		not_valid = []
		for ticker_item in ticker:
			api_request = requests.get("https://api.iex.cloud/v1/data/core/quote/" + str(ticker_item) + "?token=pk_b73b3bde6c0f4bd5aeeee63749e2fb3f")
			api = json.loads(api_request.content)
			if api[0] != None:
				api[0]['tickerid'] = ticker_item.id
				output.append(api[0])
			else:
				not_valid.append(ticker_item)
		return render(request,'add_stock.html',{'output': output, 'not_valid':not_valid})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ('Stock has been deleted!'))
	return redirect(add_stock)
