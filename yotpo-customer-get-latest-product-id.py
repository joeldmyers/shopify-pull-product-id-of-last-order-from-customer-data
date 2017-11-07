#############################
# General overview:         #
# need to get the product   #
# id from last order        #
# they purchased            #
#############################

import sys, urllib2, json, base64, datetime, copy, string, csv
from pytz import timezone, HOUR

# SHOPIFY CREDENTIALS

shopify_key = "#############"
shopify_pass = "#############"
shopify_base = "#############"

   

# Open CSV

with open('yotpo_list.csv','rU') as csv_file:
    csv_reader = csv.reader(csv_file)

    # skip first line
    next(csv_reader)

    # create new CSV to write to
    with open('yotpo_with_product_id.csv', 'w') as new_file:
        csv_writer = csv.writer(new_file, delimiter=',')

        # loop through lines
        for line in csv_reader:
            # get customer email
            email = line[0]
            name = line[1]
            
            # pass email to Shopify 

            request_url = shopify_base + "admin/customers/search.json?query=email:" + email
            request = urllib2.Request(request_url)

            auth = base64.b64encode(shopify_key + ":" + shopify_pass)
            request.add_header("Authorization", "Basic " + auth)
            contents = urllib2.urlopen(request).read()

            # Parse response, get customer's last order ID
            json_contents = json.loads(contents)

            last_order_id = str(json_contents["customers"][0]["last_order_id"])

            # take that and then ping the /admin/orders/[order_id].json

            order_request_url = shopify_base + "admin/orders/" + last_order_id + ".json"
            order_request = urllib2.Request(order_request_url)
            order_request.add_header("Authorization", "Basic " + auth)
            order_contents = urllib2.urlopen(order_request).read()
            order_json_contents = json.loads(order_contents)

            # get product id of first product they bought
            last_product_id = str(order_json_contents["order"]["line_items"][0]["product_id"])
            row_to_write = [email,name,last_product_id]
            print(row_to_write)

            csv_writer.writerow(row_to_write)
        
