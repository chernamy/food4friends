//
//  BuyPageViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 1/29/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit

class BuyPageViewController: UIViewController, UITableViewDataSource, UITableViewDelegate  {
    
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var popupView: UIView!
    @IBOutlet weak var confirmLabel: UILabel!
    
    var numServings = 2
    var descriptions: [String] = []
    var prices: [Int] = []
    var addresses: [Int] = []
    var ends: [Int] = []
    var photos: [String] = []
    var servings: [Int] = []
    var userids: [String] = []
    var image_data: [Data] = []
    
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
        let todoEndpoint: String = "http://35.1.119.53:3000/api/v1/buy"
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

                if let arrJSON = todo["items"] as? NSArray{
                    print(arrJSON.count)
                    if(arrJSON.count != 0) {
                        var i: Int = 0
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
                
                print(self.descriptions)
                print(self.prices)
                print(self.addresses)
                print(self.ends)
                print(self.photos)
                print(self.servings)
                print(self.userids)
                
                DispatchQueue.main.async() {
//                    for 0...self.photos.count {
//                        let url = URL(string: "/Users/Amy/Documents/eecs441/food4friends/xcode/images/1.png")
//                        self.downloadImage(url: url!)
//                    }
                    let url = URL(string: "https://www.thecheesecakefactory.com/assets/images/Menu-Import/CCF_FreshStrawberryCheesecake.jpg")
                    self.downloadImage(url: url!)
                }
            } catch {
                print("error trying to convert data to JSON")
                return
            }
        })
        
        task.resume()
    }

    func makePOSTCall() {
        let jsonDict = ["userid": "166392330540730", "token":"EAAFhbcIKPLABAKfLFMZALX6dlQpc7bkYA7UU6mjBCUY1vqzZAZC7wyAzOGlJSucDeOeXpjHEZCm2s4Xz1tr12QATf2oZBHaLL3cJd9299EbcpUTS5JzSIcIug6wfGILYdY92PzyDZCcbPVvXR3uctssiHa9PDiJIYZA8u0RIheHxX22grFKSjCulDsk8lm133BkL29Ej1HWvd7Wn0hARizghqKG9bjBv5qGEVFfM7ZBJaAZDZD"]
        //let data = try JSONSerialization.data(withJSONObject: jsonData, options: [])
        
        let valid = JSONSerialization.isValidJSONObject(jsonDict)
        if (valid == true) {
            print("true")
        }
        
        let loginurl = URL(string: "http://35.1.119.53:3000/api/v1/login/")!
        
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
            DispatchQueue.main.async() {
                self.makeGETCall()
            }
        }          
        task.resume()
    }
    
    
    // default view controller stuff
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        popupView.isHidden = true
        makePOSTCall()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    // Popup functions
    @IBAction func buyItem(_ sender: UIButton) {
        
        popupView.isHidden = false
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
    //TODO: make a callback function
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let cell = self.tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath) as! BuyPageCell
        print(indexPath.row)
        print(self.photos.count)
        if (self.photos.count != 0) {
            for index in 0...self.image_data.count {
                cell.photo.image = UIImage(data: image_data[0])
                
            }
        }
//        cell.photo.image = UIImage(named: self.photos[indexPath.row])
//        cell.name.text = names[indexPath.row]
        
        return cell
    }
    

}

