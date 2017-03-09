//
//  BuyPageViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 1/29/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit
import SwiftyJSON

var image_data: [Data] = []

struct buyItem {
    var numServings: Int
    var descriptions: String
    var prices: Int
    var addresses: Int
    var ends: Int
    var photos: String
    var servings: Int
    var userids: String

}

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
        image_data.append(data)
    }
}

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
    
    func downloadPics() {
        var i = 0
        while (i < self.photos.count) {
            //let path = "/Users/Amy/Documents/eecs441/food4friends/xcode/images/" + self.photos[i]
//            let imageURL = URL(fileURLWithPath: "https://img.clipartfest.com/79e2a61004f0a37c72f5220eadbfe242_death-apple-at-skyrim-nexus-apple_894-893.jpeg")
//            var data = downloadImage(url: imageURL)
            
            if let url = NSURL(string: "https://img.clipartfest.com/79e2a61004f0a37c72f5220eadbfe242_death-apple-at-skyrim-nexus-apple_894-893.jpeg"), let data = NSData(contentsOf: url as URL) {
                print (data)
            }
            
            i += 1
        }
        
        
        DispatchQueue.main.async() {
            self.tableView.reloadData()
            
        }
    }
    
    func makeGETCall() {
        let json = JSON(data: "http://0.0.0.0:3000/api/v1/buy")
        
        let todoEndpoint: String = "http://0.0.0.0:3000/api/v1/buy"
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
                print("error calling GET on /todos/1")
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
                //print("userid: " + food.userid)
                //print("photo: " + food.photo)
                //print("servings: " + todo.description)
                //print("end: " + todo.description)
                //print("price: " + todo.description)
                if let arrJSON = todo["items"] {
                    print(arrJSON.count)
                    print ("arrJSON: ")
                    if(arrJSON.count != 0) {
                        var i: Int = 0
                        while (i < arrJSON.count) {
                        
                            //TODO: FIX
                            if let aObject = arrJSON[i] as? [String: AnyObject] {
                                self.descriptions.append(aObject["description"] as! String)
                                self.prices.append(aObject["price"] as! Int)
                                //addresses.append(aObject["address"] as! String)
                                self.ends.append(aObject["end"] as! Int)
                                self.photos.append(aObject["photo"] as! String)
                                self.servings.append(aObject["servings"] as! Int)
                                self.userids.append(aObject["userid"] as! String)
 
                            }
                        
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
                
                //for index in 0...self.photos.count-1 {
                    //print(self.photos[index])
                    //self.images.append(UIImage(named: self.photos[index])!)
                //}
                //print("description: " + todo.description)
                
                self.downloadPics()
            } catch {
                print("error trying to convert data to JSON")
                return
            }
        })
        
        task.resume()
    }
    
    // Things you should query for
    //var names = ["Enchilada", "Cheesecake", "Wings"]
    //var images = [UIImage(named: "enchilada"), UIImage(named: "cheesecake"), UIImage(named: "wings")]
    var images: [UIImage] = []
    // default view controller stuff
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        popupView.isHidden = true
        makeGETCall()
        
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
            for index in 0...self.photos.count-1 {
                print(self.photos[index])
                let FoodPicURL = URL(fileURLWithPath: "../images/1.png") // We can force unwrap because we are 100% certain the constructor will not return nil in this case.
                
//                let filePath = Bundle.main.path(forResource: "/Users/Amy/Documents/eecs441/food4friends/xcode/images/1", ofType: "png")
                //let image = UIImage(contentsOfFile: "/Users/Amy/Documents/eecs441/food4friends/xcode/images/1")
                //cell.photo.image = image
                
                //let FoodPicURL = URL(fileURLWithPath: "https://img.clipartfest.com/79e2a61004f0a37c72f5220eadbfe242_death-apple-at-skyrim-nexus-apple_894-893.jpeg")

                
                //let data = try? Data(contentsOf: FoodPicURL)
                //let picture = UIImage(data: data!)
//                DispatchQueue.main.sync(){
//                    cell.photo.image = picture
//                }
                
                
//                let session = URLSession(configuration: .default)
//                let downloadPicTask = session.dataTask(with: FoodPicURL) { (data, response, error) in
//                    // The download has finished.
//                    if let e = error {
//                        print("Error downloading cat picture: \(e)")
//                    } else {
//                        // No errors found.
//                        // It would be weird if we didn't have a response, so check for that too.
//                        if let res = response as? HTTPURLResponse {
//                            print("Downloaded cat picture with response code \(res.statusCode)")
//                            if let imageData = data {
//                                // Finally convert that Data into an image and do what you wish with it.
//                                let image = UIImage(data: imageData)
//                                // Do something with your image.
//                            } else {
//                                print("Couldn't get image: Image is nil")
//                            }
//                        } else {
//                            print("Couldn't get response code for some reason")
//                        }
//                    }
//                }
//                downloadPicTask.resume()

               // images.append(UIImage(named: self.photos[index]))
            }
        }
//        cell.photo.image = UIImage(named: self.photos[indexPath.row])
//        cell.name.text = names[indexPath.row]
        
        return cell
    }
    

}

