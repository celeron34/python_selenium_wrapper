# Python 3.10.7
# selenium 4.10.0
# 2023/07/09
# 
# pip install webdriver_manager
# 
# from sys import path
# from os.path import abspath
# path.append(abspath('PATH'))
# path.append(abspath('/home/ichiru/scripts/'))
# import driver

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By as by
from selenium.webdriver.remote.webdriver import WebElement
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait

class Browser():
	def __init__(self, browserPath:str='', driverPath:str='', headless:bool=False, resultPng:bool=False, downloadDir:str='', errScreenshot:bool=False, windowSize=(720,480)):
		'''selenium 4.10.0'''
		self.resultPng = resultPng
		self.errScreenshot = errScreenshot
		options = Options()
		if browserPath: options.binary_location = browserPath						# ブラウザのエグゼファイルパス
		# options.add_argument("--blink-settings=imagesEnabled=false")				# 画像を非表示にする。
		options.add_argument("--disable-background-networking")                     # 拡張機能の更新、セーフブラウジングサービス、アップグレード検出、翻訳、UMAを含む様々なバックグラウンドネットワークサービスを無効にする。
		options.add_argument("--disable-blink-features=AutomationControlled")       # navigator.webdriver=false となる設定。確認⇒　driver.execute_script("return navigator.webdriver")
		options.add_argument("--disable-default-apps")                              # デフォルトアプリのインストールを無効にする。
		# options.add_argument("--disable-dev-shm-usage")							# ディスクのメモリスペースを使う。DockerやGcloudのメモリ対策でよく使われる。
		options.add_argument("--disable-extensions")                                # 拡張機能をすべて無効にする。
		options.add_argument("--disable-features=Translate")                        # Chromeの翻訳を無効にする。右クリック・アドレスバーから翻訳の項目が消える。
		options.add_argument("--disable-popup-blocking")							# ポップアップブロックを無効にする。
		# options.add_argument("--guest")												# ゲストモードで起動する。--incognitoとは併用不可
		if headless: options.add_argument("--headless=new")							# ヘッドレスモードで起動する。
		options.add_argument("--hide-scrollbars")									# スクロールバーを隠す。
		options.add_argument("--ignore-certificate-errors")							# SSL認証(この接続ではプライバシーが保護されません)を無効
		options.add_argument("--incognito")											# シークレットモードで起動する。--guestとは併用不可
		options.add_argument("--mute-audio")										# すべてのオーディオをミュートする。
		options.add_argument("--no-default-browser-check")							# アドレスバー下に表示される「既定のブラウザとして設定」を無効にする。
		options.add_argument("--propagate-iph-for-testing")							# Chromeに表示される青いヒント(？)を非表示にする。
		# options.add_argument("--start-maximized")									# ウィンドウの初期サイズを最大化。--window-position, --window-sizeの2つとは併用不可
		# options.add_argument("--user-agent=" + UserAgent(os="windows").chrome)	# ユーザーエージェントの指定。
		# options.add_argument("--window-position=100,100")							# ウィンドウの初期位置を指定する。--start-maximizedとは併用不可
		options.add_argument(f"--window-size={windowSize[0]},{windowSize[1]}")		# ウィンドウの初期サイズを設定する。--start-maximizedとは併用不可
		# options.add_argument("--autoplay-policy=user-required")						# 自動再生を許可しない
		# options.add_argument("--autoplay-policy=disallowed")						# 自動再生を許可しない
		options.add_experimental_option("excludeSwitches", ["enable-automation"])	# Chromeは自動テスト ソフトウェア~~　を非表示
		# options.set_capability("browserVersion", "123")							# ブラウザのバージョンを指定する。
		
		
		prefs = {
			"credentials_enable_service": False,									# パスワード保存のポップアップを無効
			"plugins.always_open_pdf_externally": True,								# Chromeの内部PDFビューアを使わない(＝URLにアクセスすると直接ダウンロードされる)
			"download.prompt_for_download": False,									# ダウンロード前に確認 False:しない True:する
			"download_bubble.partial_view_enabled": False,							# ダウンロードが完了したときの通知(吹き出し/下部表示)を無効にする。
			# "profile.default_content_setting_values.media_stream_mic": 2,  # マイクを無効化
			# "profile.default_content_setting_values.media_stream_camera": 2,  # カメラを無効化
			"profile.default_content_setting_values.autoplay": 2,  # 自動再生メディアをブロック
			# "profile.default_content_setting_values.notifications": 2, # 通知
		}
		if downloadDir != '':
			prefs["savefile.default_directory"] = downloadDir						# ダイアログ(名前を付けて保存)の初期ディレクトリを指定
			prefs["download.default_directory"] = downloadDir						# ダウンロード先を指定
		print(prefs)
		options.add_experimental_option("prefs", prefs)
		
		if driverPath != '':
			service = Service(driverPath)
			self.driver = webdriver.Chrome(options=options, service=service)
		else:
			self.driver = webdriver.Chrome(options=options)
		# self.wait = WebDriverWait(driver=self.driver, timeout=30)

	def __enter__(self):
		return self

	def __exit__(self, *args):
		self.driver.quit()

	def __del__(self):
		self.driver.quit()

	def getXPath(self, XPATH:str, timeout:int=10) -> list[WebElement]:
		''' XPath を指定して WebElement を取得
		複数: list[WebElement]
		１つ: WebElement
		無し: None
		'''
		try:
			self.driver.implicitly_wait(timeout)
			elements = self.driver.find_elements(by.XPATH, XPATH)
		except Exception as e:
			if self.errScreenshot: self.driver.save_screenshot('error result.png')
			return e
		return elements
		
	''' 指定した URL にアクセス'''
	def jumpURL(self, url:str):
		ret = self.driver.get(url)
		# self.wait.until(EC.presence_of_all_elements_located)
		return ret
	
	''' 指定した XPath または WebElement のテキストを取得 '''
	def getXPathText(self, XPATH:str|WebElement, timeout:int=10) -> str | list[str]:
		try:
			if type(XPATH) == WebElement: return XPATH.text
			self.driver.implicitly_wait(timeout)
			elements = self.driver.find_elements(by.XPATH, XPATH)

			if len(elements) == 1:
				return elements[0].text
			elif len(elements) == 0:
				return ''
			else:
				ret = []
				for i in range(len(elements)):
					ret.append(elements[i].text)
				return ret
			
		except Exception as e:
			if self.errScreenshot: self.driver.save_screenshot('error result.png')
			return e
		

	'''指定した XPath または WebElement をクリック'''
	def clickXPath(self, XPATH:str|WebElement, timeout:int=10):
		try:
			self.driver.implicitly_wait(timeout)
			if type(XPATH) == WebElement: XPATH.click()
			self.driver.find_element(by.XPATH, XPATH).click()
		except Exception as e:
			if self.errScreenshot: self.driver.save_screenshot('error result.png')
			return e

	'''指定した XPath または WebElement に入力'''
	def sendXPath(self, XPATH:str|WebElement, key, timeout:int=10):
		try:
			self.driver.implicitly_wait(timeout)
			if type(XPATH) == WebElement: return XPATH.send_keys(key)
			self.driver.find_element(by.XPATH, XPATH).send_keys(key)
		except Exception as e:
			if self.errScreenshot: self.driver.save_screenshot('error result.png')
			return e

	''' 指定した XPath のフレームへ移動'''
	def swFrame(self, XPATH:str, timeout:int=10):
		try:
			self.driver.implicitly_wait(timeout)
			self.driver.switch_to.frame(self.driver.find_element(by.XPATH, XPATH))
		except Exception as e:
			if self.errScreenshot: self.driver.save_screenshot('error result.png')
			return e

	''' 現在のフレームの親フレームに移動'''
	def parentFrame(self):
		try:
			self.driver.switch_to.parent_frame()
		except Exception as e:
			if self.errScreenshot: self.driver.save_screenshot('error result.png')
			return e

	def getXPathAttr(self, XPATH:str, atr:str, timeout:int=10) -> str | list[str]:
		try:
			self.driver.implicitly_wait(timeout)
			elements = self.driver.find_elements(by.XPATH, XPATH)
			if len(elements) == 1:
				return elements[0].get_attribute(atr)
			elif len(elements) == 0:
				return ''
			else:
				ret = []
				for i in range(len(elements)):
					ret.append(elements[i].get_attribute(atr))
				return ret
		except Exception as e:
			if self.errScreenshot: self.driver.save_screenshot('error result.png')
			return e
	
	def scrollTop(self):
		try:
			self.driver.execute_script('window.scrollTo(0,0);')
		except Exception as e:
			if self.errScreenshot: self.driver.save_screenshot('error result.png')
			return e

	def refresh(self):
		self.driver.refresh()

	def getSorce(self) -> str:
		return self.driver.page_source

	def getURL(self) -> str:
		return self.driver.current_url

	def screenshot(self, path:str):
		self.driver.save_screenshot(path)

	def selectList(self, XPATH:str, VALUE:str):
		Select(self.driver.find_element(by.XPATH, XPATH)).select_by_value(VALUE)

	def back(self, re:int=1):
		for _ in range(re):
			self.driver.back()
	
	def addLocalstrage(self, key, value):
		self.driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")

	def getLocalstrage(self, key):
		return self.driver.execute_script(f"return window.localStorage.getItem('{key}');")

	def quit(self):
		if self.resultPng:
			try:
				self.driver.save_screenshot('./result.png')
			except Exception as e:
				print(e)
		self.driver.quit()
		