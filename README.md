# spotscraper

## add local libraries first
mkdir lib
pip3 install pandas bs4 -t lib/

## change the path variable in scraper.py
Change the path that you created above to be appended to the system path - best to create an absolute path
sys.path.append('/opt/spotscraper/lib')

## using
Running the script outputs text in JSON format. You can run this daily via e.g. crontab at e.g. 14h UTC, then the market prices are already set. I personally then parse the file in node-red, to flush it to an influxDB; and use that to overlay it on my power graphs in grafana.
