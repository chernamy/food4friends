//
//  BuyPageViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 1/29/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit

var server = "http://35.1.142.128:3000"

class BuyPageViewController: UIViewController, UITableViewDataSource, UITableViewDelegate  {
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var popupView: UIView!
    @IBOutlet weak var confirmLabel: UILabel!
    
    var descriptions: [String] = []
    var prices: [Int] = []
    var addresses: [Int] = []
    var ends: [Int] = []
    var photos: [String] = []
    var servings: [Int] = []
    var userids: [String] = []
    var image_data: [Data] = []
    var totalNumItems = 0
    var servingsBought = -1
    var itemNumberBought = -1
    
    func getDataFromUrl(url: URL, completion: @escaping (_ data: Data?, _  response: URLResponse?, _ error: Error?) -> Void) {
        URLSession.shared.dataTask(with: url) {
            (data, response, error) in
            completion(data, response, error)
            }.resume()
    }
    
    func downloadImage(url: URL) {
        print("Download Started")
        getDataFromUrl(url: url) { (data, response, error)  in
            guard let data = data, error == nil else { return }
            print(response?.suggestedFilename ?? url.lastPathComponent)
            print("Download Finished")
            self.image_data.append(data)
            DispatchQueue.main.async() { () -> Void in
                self.tableView.reloadData()
            }
        }
    }
    
    func makeGETCall() {
        let todoEndpoint: String = server + "/api/v1/buy"
        guard let url = URL(string: todoEndpoint) else {
            print("Error: cannot create URL")
            return
        }
        let urlRequest = URLRequest(url: url)
        
        let config = URLSessionConfiguration.default
        let session = URLSession(configuration: config)
        
        let task = session.dataTask(with: urlRequest, completionHandler: {
            (data, response, error) in
            // do stuff with response, data & error here
            // check for any errors
            guard error == nil else {
                print("error calling GET on /api/v1/buy")
                print(error)
                return
            }
            // make sure we got data
            guard let responseData = data else {
                print("Error: did not receive data")
                return
            }
            do {
                guard let todo = try JSONSerialization.jsonObject(with: responseData, options: []) as? [String: AnyObject] else {
                    print("error trying to convert data to JSON")
                    return
                }
                
                //TODO: add to addresses array
                if let arrJSON = todo["items"] as? NSArray{
                    print(arrJSON.count)
                    self.totalNumItems = arrJSON.count
                    if(arrJSON.count != 0) {
                        for item in (arrJSON as? [[String:Any]])!{
                            print(item)
                            self.descriptions.append(item["description"] as! String)
                            self.prices.append(item["price"] as! Int)
                            //self.addresses.append(item["address"] as! Int)
                            self.ends.append(item["end"] as! Int)
                            self.photos.append(item["photo"] as! String)
                            self.servings.append(item["servings"] as! Int)
                            self.userids.append(item["userid"] as! String)
                        }
                    }
                }
                
                DispatchQueue.main.async() {
                    var i = 0
                    while (i < self.totalNumItems) {
                        print("image names: " + self.photos[i])
                        let url_string = server + "/static/" + self.photos[i]
                        print("url: " + url_string)
                        let url = URL(string: url_string)
                        self.downloadImage(url: url!)
                        i += 1
                    }
                }
            } catch {
                print("error trying to convert data to JSON")
                return
            }
        })
        
        task.resume()
    }
    
    func makePOSTCall(jsonDict: Dictionary<String, Any>, api_route: String, login: Bool) {
        let loginurl = URL(string: server + api_route)!
        
        let request = NSMutableURLRequest(url: loginurl)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let jsonData = try? JSONSerialization.data(withJSONObject: jsonDict, options: .prettyPrinted) {
            request.httpBody = jsonData
        }
        
        let task = URLSession.shared.dataTask(with: request as URLRequest){ data,response,error in
            if error != nil{
                print(error?.localizedDescription)
                return
            }
            
            do {
                if let json = try JSONSerialization.jsonObject(with: data!, options: .mutableContainers) as? NSDictionary {
                    let resultValue:String = json["info"] as! String;
                    print("result: \(resultValue)")
                }
            } catch let error as NSError {
                print(error)
            }
            if (login == true) {
                DispatchQueue.main.async() {
                    self.makeGETCall()
                }
            } else {
                self.tableView.reloadData()
            }
        }
        task.resume()
    }
    
    func refreshView() {
        self.descriptions = []
        self.prices = []
        self.addresses = []
        self.ends = []
        self.photos = []
        self.servings = []
        self.userids = []
        self.image_data = []
        self.totalNumItems = 0
        self.servingsBought = -1
        self.itemNumberBought = -1
        
        self.makeGETCall()
    }
    
    // default view controller stuff
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        popupView.isHidden = true
        // post to login route
        let jsonDict = ["userid": "166392330540730", "token":"EAAFhbcIKPLABAKfLFMZALX6dlQpc7bkYA7UU6mjBCUY1vqzZAZC7wyAzOGlJSucDeOeXpjHEZCm2s4Xz1tr12QATf2oZBHaLL3cJd9299EbcpUTS5JzSIcIug6wfGILYdY92PzyDZCcbPVvXR3uctssiHa9PDiJIYZA8u0RIheHxX22grFKSjCulDsk8lm133BkL29Ej1HWvd7Wn0hARizghqKG9bjBv5qGEVFfM7ZBJaAZDZD"]
        makePOSTCall(jsonDict: jsonDict, api_route: "/api/v1/login/", login: true)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func cancelPopup(_ sender: Any) {
        popupView.isHidden = true
    }
    
    // For creating the table view
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // return how many rows in the table
        if self.photos.count == 0 {
            return 0
        }
        return self.photos.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = self.tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath) as! BuyPageCell
        popupView.isHidden = true
        cell.photo.image = UIImage(data: image_data[indexPath.row])
        cell.name.text = self.descriptions[indexPath.row]
        cell.price.text = "Price: $" + String(self.prices[indexPath.row])
        cell.servingsAvailable.text = "Servings: " + String(self.servings[indexPath.row])
        cell.servingsBought.text = ""
        return cell
    }
    
    @IBAction func buyItemFinal(_ sender: Any) {
        let sellerid = self.userids[itemNumberBought]
        let buyerid = "166392330540730"
        let jsonDict = ["sellerid": sellerid, "buyerid": buyerid, "servings": self.servingsBought] as [String : Any]
        makePOSTCall(jsonDict: jsonDict, api_route: "/api/v1/buy/", login: false)
    }
    
    func tableView(_ tableView: UITableView, willSelectRowAt indexPath: IndexPath) -> IndexPath? {
        popupView.isHidden = false
        itemNumberBought = indexPath.row
        let cell = tableView.cellForRow(at: indexPath) as! BuyPageCell
        self.servingsBought = Int(cell.servingsBought.text!)!
        print(indexPath.row)
        return indexPath
    }
}

