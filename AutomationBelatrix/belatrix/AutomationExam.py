# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
import time 

from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains  

class Ebay(unittest.TestCase):
    
     def setUp(self):
        self.driver = webdriver.Firefox(executable_path=r'C:\Users\ea8034\Desktop\belatrix\geckodriver.exe')
     
     def test_ebay(self):
        driver = self.driver   
        #1 Enter to Ebay
        driver.get("https://www.ebay.com")
        #2 Search for shoes
        driver.find_element_by_id("gh-ac").send_keys("shoes")
        driver.find_element_by_id("gh-btn").click()
        time.sleep(2)
        #3 Select brand PUMA
        driver.find_element_by_id("e1-51").click()
        time.sleep(2)
        #4 Select size 10
        driver.find_element_by_id("e1-29").click()
        time.sleep(2)
        #5 Print the number of results
            #Like a image
        driver.save_screenshot("screenshot.png")
            #Like a text
        for elem in driver.find_elements_by_xpath('.//span[@class = "rcnt"]'):
            print "Print the number of results:" + elem.text
            
        print "\n"              
        time.sleep(2)
        #6 Order by price ascendant
        driver.find_element_by_id("DashSortByContainer").click()
        items = driver.find_elements_by_xpath("//ul[@id = 'SortMenu']//li[not(@class)]//a[@value = '15']")
        for item in items:
            item.click()
            
        #7 Assert the order taking the first 5 results    
        text_contents = [el.text for el in driver.find_elements_by_xpath("//ul[@id='GalleryViewInner']/li")]
        number = 0
        
        for text in text_contents:
            number = number + 1 
            print "Result "+str(number)+": "+ text
            if number == 5: break  
         
        print "\n"              
        self.assertEqual(5, number)
       
       
        #8 Take the first 5 products with their prices and print them in console.
        
        counter = 1
        listProductName  = []
        listProduct  = []
        while counter <= 5:
            
            DescProductName = [elX.text for elX in driver.find_elements_by_xpath("/html/body/div[5]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/w-root/div/div/ul/li["+str(counter)+"]/div/div[2]/h3/a")]    
            if DescProductName is None or (not DescProductName):
                   #Cuando aparece valor Span PATROCINADO 
                   DescProductName = [elX.text for elX in driver.find_elements_by_xpath("/html/body/div[5]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/w-root/div/div/ul/li["+str(counter)+"]/div/div[3]/h3/a")] 
            
            for pn in DescProductName:
                print "Product Name "+str(counter)+":"+pn
            
            DescPrice = [elX.text for elX in driver.find_elements_by_xpath("/html/body/div[5]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/w-root/div/div/ul/li["+str(counter)+"]/div/div[3]/div[2]/div/span[1]/span")]    
            if (DescPrice is None) or (not DescPrice):
                   #Cuando aparece valor Mejor oferta 
                   DescPrice = [elX.text for elX in driver.find_elements_by_xpath("/html/body/div[5]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/w-root/div/div/ul/li["+str(counter)+"]/div/div[3]/div[2]/span[1]")]    
                   
            for p in DescPrice:
                print "Price "+str(counter)+":"+p
            
            
            
            
            DescPriceShip = [elX.text for elX in driver.find_elements_by_xpath("/html/body/div[5]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/w-root/div/div/ul/li["+str(counter)+"]/div/div[4]/div[1]/div")]    
            for ps in DescPriceShip:
                print "Shipping "+str(counter)+":"+ps
            
            
            
            print "\n" 
            PrecioTotal=float(p.encode('utf-8').replace("S/.", "").strip())+ 3.25*float(ps.encode('utf-8').replace("+USD", "").replace("envío", "").strip())
            listProduct.append(Product(pn.encode('utf-8'),p.encode('utf-8'),ps.encode('utf-8'),PrecioTotal))
            counter=counter+1
        
        #9 Order and print the products by name (ascendant)
        print "\nProductos Sin Ordenar"     
        lista(listProduct)      
        print "\nProductos Ordenados Acendentemente por: Name"
        listaByNameAsc = sorted(listProduct,key=lambda objeto: objeto.nombre)
        lista(listaByNameAsc)
        #10 Order and print the products by price in descendant mode
        print "\nProductos Ordenados Descendentemente por: Precio Con Envio en Soles S/. (Precio Sin Envio + Envio*3.25)"
        listaByPrecioAsc = sorted(listProduct,key=lambda objeto: float(objeto.precioConEnvio), reverse=True)
        lista(listaByPrecioAsc)
     
     def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()


class Product():
    def __init__(self, nombre, precio,envio,precioConEnvio):
        self.nombre = nombre
        self.precio = precio
        self.envio = envio
        self.precioConEnvio = precioConEnvio
    def __str__(self):
        return "%s | %s | %s | %s" % (self.nombre, self.precio, self.envio, self.precioConEnvio)
 
def lista(vv):   
    for v in vv:
        print (v)
    