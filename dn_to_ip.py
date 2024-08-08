import tkinter as tk
from ipwhois import IPWhois
import whois
import socket


# ^^ importing

window = tk.Tk()
info = tk.Label(text="Enter info to find the IP of a domain name or vice versa!")
info.place(x=10,y=10)

#taking the code and associating it with a country name
country_code_names = {
    'US': 'United States',
    'CA': 'Canada',
    'GB': 'United Kingdom',
    'FR': 'France',
    'DE': 'Germany',
    'JP': 'Japan',
    'CN': 'China',
    'IN': 'India',
    'AU': 'Australia',
    'BR': 'Brazil',
    # add more
}

#socket finding IP Address of domain name:
def get_ip(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return "No valid IP found"

### introduction section, below gets into inputting
def find():
   
    entry_text = entry.get().strip()  # Calls the entry
    print(f"Entry text is: {entry_text}")  # Seeing what the entry is

    # Clear previous results labels if they exist
    if hasattr(find, 'results_label'):
        find.results_label.destroy()
    if hasattr(find, 'results_label2'):
        find.results_label2.destroy()

    # Input validation
    if not entry_text:  # Check if input is empty
        find.results_label = tk.Label(window, text="Error: Please enter an IP address or domain name.")
        find.results_label.place(x=75, y=125)
        return

    # Determine if the input is an IP address or a domain name
    if entry_text.count('.') == 3:  # Simple check for IP address (IPv4)
        try:
            ip_obj = IPWhois(entry_text)
            resultswhois = ip_obj.lookup_rdap()  # Get WHOIS info for the IP address
            print(f"IP WHOIS Results: {resultswhois}")  # Debugging info for the results

            w = whois.whois(entry_text)
            print(f"results of whois: {w}")

            domain_name = w.domain if w.domain is not None and w.domain != "" else "No domain found"

            country_code = resultswhois.get('asn_country_code', 'No country code found')
            country_name = country_code_names.get(country_code, 'Unknown country code')

            state = w.state if w.state else "No state found"

            ip_address = entry_text  # The input is the IP address

            # Creating the result labels
            find.results_label2 = tk.Label(window, text=f"Domain Name: {domain_name}\nCountry: {country_name}\nState: {state}")
            find.results_label2.place(x=75, y=175)

        except Exception as e:
            find.results_label = tk.Label(window, text=f"Error retrieving IP WHOIS data: {e}")
            find.results_label.place(x=75, y=125)

    else:  # Treat as domain name
        try:
            # Using the whois library to retrieve domain information
            w = whois.whois(entry_text)
            print(f"results of whois: {w}")

            country_code = w.get('country', 'No country code found')
            country_name = country_code_names.get(country_code, 'Unknown country code')
            state = w.state if w.state else "No state found"

            # Get the IP address for the domain
            ip_address = get_ip(entry_text)
            print(f"IP Address found: {ip_address}")  # Debugging info for IP address

            # Creating the result labels
            find.results_label2 = tk.Label(window, text=f"IP Address: {ip_address}\nCountry: {country_name}\nState: {state}")
            find.results_label2.place(x=75, y=175)

        except Exception as e:
            find.results_label = tk.Label(window, text=f"Error retrieving data: {e}")
            find.results_label.place(x=75, y=125)

    find.results_label = tk.Label(window, text="Here is what we found for " + entry_text + ":")
    find.results_label.place(x=75, y=125)
    
    
    def clear_entry(): #clears out the entry box and labels
        entry.delete(0, tk.END)
        if clear:
            clear.destroy()
        # Clear result labels if they exist
        if hasattr(find, 'results_label'):
            find.results_label.destroy()
        if hasattr(find, 'results_label2'):
            find.results_label2.destroy()

    clear = tk.Button(window,text="Clear results",command=clear_entry)
    clear.place(x=175, y=100)


entry = tk.Entry(window)
entry.place(x=100,y=50)
search = tk.Button(window,text="Search",command=find)
search.place(x=100, y=100)
    

##### ending section


def exit(): #another exit to the application
    window.destroy()

done = tk.Button(text="Done", command=exit)
done.pack(side="bottom")
    

window.title("Searching...") #window's text
window.geometry('350x300') #window size
window.resizable(False, False) #disallow resizing of window
window.mainloop() #shows  up

