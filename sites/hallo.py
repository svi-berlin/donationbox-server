import os
import subprocess
import time
from flask import Flask, render_template, Markup, request, url_for

app = Flask(__name__)  
app.config['DEBUG'] = True

@app.route("/")  
def hello():
	templateData = {
		'content' : get_fortunes(),
		'compare' : '-*-'
	}
	return render_template('main.html', **templateData)  

@app.route('/spider/', methods=['POST'])
def spider():
    spiderUrl=request.form['spiderUrl']
    os.system("sudo python /home/pi/spider/spider.py " + spiderUrl)
    return render_template('form_action.html', spiderUrl=spiderUrl)

@app.route("/spiderform/")
def form():
        return render_template('form_submit.html')

@app.route('/compare/', methods=['POST'])
def compare():
        email = request.form['email']
        minutes = request.form['minutes']
        url = request.form['url']
        out = get_compare(email, minutes, url)
        templateData = {
		'out' : out,
                'email' : email,
                'minutes': minutes,
                'url': url
        }
        return render_template('form_compare_action.html', **templateData)

@app.route("/compareform/")
def form_compare():
        return render_template('form_compare_submit.html')

def take_webshot(url, name):
    cmd = ["python","/home/pi/flask/sites/compare/webshot.py",url,name]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()

def send_email(email):
    cmd = ["python","/home/pi/flask/sites/compare/compare_and_send_email.py",email]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out

def get_compare(email, minutes, url):
    take_webshot(url, 'before')
    time.sleep(float(minutes) * 60)
    take_webshot(url, 'after')
    time.sleep(3)
    out = send_email(email)
    return out

def get_fortunes():
	fh = open("/usr/local/bin/donationbox/fortunes.txt", "r")
	content = ''
	for line in reversed(open("/usr/local/bin/donationbox/fortunes.txt").readlines()):
    		line = line.replace('\n', '<br />')
		content += line.rstrip()
	
	fortunes = Markup(content)
	return fortunes

if __name__ == "__main__":  
   app.run('0.0.0.0')  
