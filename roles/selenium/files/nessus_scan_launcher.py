from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from optparse import OptionParser
from time import sleep
from pdb import set_trace




def parse_cli_args():
    parser = OptionParser()
    parser.add_option("-cfg", "--config",
                    dest="config_file")
    parser.add_option("-su", "--selenium-url",
                    dest="selenium_url")
    parser.add_option("-u", "--nessus-url",
                    dest="server_url")
    parser.add_option("-c", "--customer",
                    action="append",
                    dest="customer",
                    help="customer folder to scan")
    parser.add_option("-s", "--scan-name",
                    dest="scan_name")

    (options, args) = parser.parse_args()
    return {
        'config_file': options.config_file,
        'selenium_url': options.selenium_url or 'http://192.168.0.101:4444/wd/hub',
        'server_url': options.server_url,
        'customer': options.customer[0],
        'scan_name': options.scan_name,
    }


"""
remote_selenium_server = 'http://192.168.0.101:4444/wd/hub'
username, password = '{{ user_name }}', '{{ password }}'
customer = 'Exelegent-Systems'
scan_type = 'CPA'
scan_name = '3. Credentialed Patch Audit - ns1'
"""



if __name__ == '__main__':
    options = parse_cli_args()

    driver = webdriver.Remote(
        command_executor=options['selenium_url'],
        desired_capabilities=DesiredCapabilities.CHROME
    )

    # new
    driver.get(options['server_url'])
    sleep(5)

    # authentication
    login = driver.find_element_by_class_name('login-username')
    login.clear()
    login.send_keys(options['username'] + Keys.RETURN)
    passwd = driver.find_element_by_class_name('login-password')
    passwd.clear()
    passwd.send_keys(options['password'] + Keys.RETURN)
    sleep(10)

    # customer scans folder
    scan_list = driver.find_elements_by_partial_link_text(options['customer'])[0]
    scan_list.send_keys(Keys.RETURN)
    scans = driver.find_element_by_class_name("scans.dataTable.no-footer")
    scans_rows = scans.find_elements_by_tag_name('tr')

    # customer scan type
    for row in scans_rows:
        cols = row.find_elements_by_tag_name("td")
        if len(cols) > 0:
            print(cols[2].text)
            if cols[2].text == options['scan_name']:
                scan, scan_web_name, scan_launcher = row, cols[2].text, cols[-2]
                break;

    # launch desired scan
    customer_scan_launcher = scan.find_elements_by_tag_name('td')[-2]
    customer_scan_launcher.click()



