import csv
import jinja2
import textwrap

def wraptext(text):
    string = text
    wrapper = textwrap.TextWrapper(width=52)
    word_list = wrapper.wrap(text=string)
    string = '\n '.join(word_list)
    return string

def get_table():
    data = []
    with open('csv_files/RCM_dictionary.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))

    for row in range(len(data)):
        for cell in range(len(data[row])):
            if '\n' not in data[row][cell]:
                data[row][cell] = wraptext(data[row][cell])

    return data

def main():
    data = get_table()
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )

    template = template_env.get_template('table.html')
    msg = 'didn\'t work'
    # render data from config file
    headers = data[0]
    data = data[1:-1]
    msg = template.render({"headers": headers, "data": data})

    msg = msg.replace("0.0 SQL Filters", "<b>0.0 SQL Filters</b>")
    msg = msg.replace("0.1 Exclude Admin Financial Class ?", 
                "<span style=\"color:red\">0.1 Exclude Admin Financial Class ?</span>")
    file_out = open("index.html", "w+")
    file_out.write(msg)
    file_out.close()

if __name__ == "__main__":
    main()