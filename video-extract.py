from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import youtube_dl
from tqdm import tqdm

profile = FirefoxProfile()
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")
profile.set_preference("browser.download.folderList", 2);

browser = webdriver.Firefox(executable_path=r'C:\Users\...\Downloads\geckodriver\geckodriver.exe',
                            firefox_profile=profile)


# inputs
url_path = 'https://www.coursera.org/learn/excellence-operationnelle/home/welcome'
path_to_folder = 'G:/coursera'
# end of inputs

url_path = '/'.join(url_path.split('/')[0:len(url_path.split('/'))-1])

# Weeks list
wl = [1,2,3]

# Extracting data from Coursera
for week in tqdm(wl):
    try:
        url = url_path + '/week/' + str(week)
        browser.get(url)
        time.sleep(8)

        # Getting all the links for the week
        text = browser.find_elements_by_css_selector("div.rc-ModuleLessons a")
        l1 = []
        for element in text:
            url2 = element.get_attribute('href')
            l1.append(url2)

        # Making a folder
        try:
            path = path_to_folder + 'Week' + str(week)
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

        i = 1

        # Getting and download file link
        for pg in tqdm(l1):
            try:
                browser.get(pg)
                # wait
                time.sleep(8)
                # Click on download button
                css = '.rc-DownloadsDropdown'
                dl = browser.find_element_by_css_selector(css)
                dl.click()
                # Wait time
                time.sleep(8)

                # Click on Lecture Video
                css = '.bt3-dropdown-menu > a:nth-child(1)'
                dl = browser.find_element_by_css_selector(css)
                time.sleep(8)
                dl2 = dl.get_attribute('href')
                #print (dl2)

                # Download the file
                path2 = path + '//' + str(i) + '-' + pg.split('/')[-1]
                i += 1
                print(path2)
                ydl_opts = {'outtmpl': path2}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([dl2])

            except:
                print('skipped ' + pg)

    except: print('week {} not found' .format(week))


