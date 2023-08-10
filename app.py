from flask import Flask, request, redirect, render_template , render_template_string
import csv
import os
import sqlite3
import secrets
import webbrowser
app = Flask(__name__)

# Dictionary to store masked links
'''
    Key = Masked Link
    Value->List = Original Link , Click Count
'''
link_mask = {}

# Set up SQLite database for storing click data
db_conn = sqlite3.connect("click_data.db")
db_cursor = db_conn.cursor()
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS clicks (
        masked_link TEXT,
        original_link TEXT,
        click_count INTEGER DEFAULT 0,
        PRIMARY KEY (masked_link)
    )
""")
db_conn.commit()

# Function to generate masked links
def generate_masked_link(original_link):
    '''We can use the Orginal Link to generate a masked link'''
    new_domain = "http://masked-link.com/"  # Replace with your masked domain
    masked_link = new_domain + secrets.token_hex(6)  # Use a more secure method in production
    return masked_link

@app.route("/", methods=["GET", "POST"])
def index():
    if(request.method == "POST"):
        # print(request.files)
       
        
        file = request.files['csv_file']
        # print(file)
        if file.filename == '':
            return "No selected file"

        if file:
            csv_data = file.read().decode('utf-8')
            csv_rows = csv_data.splitlines()


            global link_mask
            
            for row in csv.reader(csv_rows):
                original_link = (row[0])  
                masked_link = generate_masked_link(original_link)
                print("Here")
                link_mask[masked_link] = [original_link, 0]
                # insert_query = "INSERT OR IGNORE INTO clicks (masked_link, original_link) VALUES (?, ?)"
                # db_cursor.execute(insert_query, (masked_link, original_link))
                # db_cursor.execute("INSERT OR IGNORE INTO clicks (masked_link, original_link) VALUES (?, ?)", (masked_link, original_link))
                
                print("Inserted Record : ", masked_link, original_link)
            # db_conn.commit()
        return render_template("Dashboard.html", link_mask=link_mask)
    return render_template("index.html")

@app.route("/masked_link/<masked_link>" , methods=["GET"])
def redirect_to_original(masked_link):
    print(masked_link)
    base = "http://masked-link.com/"
    if((base + masked_link) in link_mask):
        link_mask[(base + masked_link)][1] += 1
        print(link_mask)
        webbrowser.open_new_tab(link_mask[(base + masked_link)][0])
        # render_template_string('<a href="{{ https://www.google.com }}" target="_blank">Click here to open in a new tab</a>', url=link_mask[(base + masked_link)][0])
        # return redirect(link_mask[(base + masked_link)][0])
    else:
        return "Invalid Masked Link"
    
    
    # return to the dashboard html route
    return render_template("Dashboard.html", link_mask=link_mask)
    return "Hittin this route"

if __name__ == "__main__":
    app.run(debug=True)
