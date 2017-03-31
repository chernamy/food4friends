//
//  BuyPageViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 1/29/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit

func hexStringToUIColor (hex:String) -> UIColor {
    var cString:String = hex.trimmingCharacters(in: .whitespacesAndNewlines).uppercased()
    if (cString.hasPrefix("#")) {
        cString.remove(at: cString.startIndex)
    }
    if ((cString.characters.count) != 6) {
        return UIColor.gray
    }
    var rgbValue:UInt32 = 0
    Scanner(string: cString).scanHexInt32(&rgbValue)
    return UIColor(
        red: CGFloat((rgbValue & 0xFF0000) >> 16) / 255.0,
        green: CGFloat((rgbValue & 0x00FF00) >> 8) / 255.0,
        blue: CGFloat(rgbValue & 0x0000FF) / 255.0,
        alpha: CGFloat(1.0)
    )
}

struct Address {
    var lattitude: String
    var longitude: String
    init(input: String) {
        print(input)
        let array_input = input.characters.split(separator: ",")
        lattitude = String(array_input[0])
        longitude = String(array_input[1])
        print(lattitude)
        print(longitude)
    }
}

class BuyPageViewController: UIViewController, UITableViewDataSource, UITableViewDelegate  {
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var popupView: UIView!
    @IBOutlet weak var confirmLabel: UILabel!
    @IBOutlet weak var errorMessage: UILabel!
    @IBOutlet weak var errorView: UIView!
    
    var descriptions: [String] = []
    var prices: [Int] = []
    var addresses: [Address] = []
    var ends: [String] = []
    var photos: [String] = []
    var servings: [Int] = []
    var userids: [String] = []
    var image_data: [Data] = []
    var totalNumItems = 0
    var servingsBought = -1
    var itemNumberBought = -1
    var getInProgress: Bool = false
    var photoExists: Bool = false
    var non_existing_photos: [String] = []
    
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
        }
    }
    
    func refreshData() {
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
    
    func makeGETCall() {
        let todoEndpoint: String = server + "/api/v1/buy/"
        self.getInProgress = true
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
                print("error calling GET on /api/v1/buy/")
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
                            self.addresses.append(Address(input: item["address"] as! String))
                            let epochTime = item["end"] as! Double
                            self.photos.append(item["photo"] as! String)
                            self.servings.append(item["servings"] as! Int)
                            self.userids.append(item["userid"] as! String)
                            let currentEpoch = NSDate().timeIntervalSince1970
                            let diffEpoch = Double(epochTime) - Double(currentEpoch)
                            var time = NSDate(timeIntervalSince1970: Double(diffEpoch))
                            var timeLeft = String(describing: time)
                            let timeArr = timeLeft.characters.split(separator: " ")
                            self.ends.append(String(timeArr[1]))
                        }
                    }
                }
                
                DispatchQueue.main.async() {
                    var i = 0
                    while (i < self.totalNumItems) {
                        print("image names: " + self.photos[i])
                        let url_string = server + "/" + self.photos[i]
                        print("url: " + url_string)
                        let url = URL(string: url_string)
                        self.downloadImage(url: url!)
                        i += 1
                    }
                }
                while (self.image_data.count != self.totalNumItems) {
                    sleep(1)
                }
                
                DispatchQueue.main.async() { () -> Void in
                    self.getInProgress = false
                    self.tableView.reloadData()
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
                print("buypageviewcontroller POST session creation error: ")
                print(error?.localizedDescription)
                return
            }
            
            do {
                if let json = try JSONSerialization.jsonObject(with: data!, options: .mutableContainers) as? NSDictionary {
                    if (json["error"] != nil) {
                        print("jsonseriaization error: ")
                        print(json["error"])
                        DispatchQueue.main.async() {
                            self.popupView.isHidden = true
                            self.errorView.isHidden = false
                            self.errorMessage.text = json["error"] as! String?
                            self.errorMessage.lineBreakMode = .byWordWrapping
                            self.errorMessage.numberOfLines = 0
                        }
                        
                    } else {
                        let resultValue:String = json["info"] as! String;
                        print("result: \(resultValue)")
                        self.popupView.isHidden = true
                        self.tabBarController?.selectedIndex = 4
                        self.refreshData()
                    }
                }
            } catch let error as NSError {
                print("buypageviewcontroller POST catch error: ")
                print(error)
            }
            //self.tableView.reloadData()
        }
        task.resume()
    }
    
    func animateViewMoving(up:Bool, moveValue: CGFloat) {
        var movementDuration:TimeInterval = 0.3
        var movement:CGFloat = (up ? -moveValue: moveValue)
        UIView.beginAnimations("animateView", context: nil)
        UIView.setAnimationBeginsFromCurrentState(true)
        UIView.setAnimationDuration(movementDuration)
        self.view.frame = self.view.frame.offsetBy(dx: 0, dy: movement)
        UIView.commitAnimations()
    }
    
    func textFieldDidBeginEditing(textField: UITextField) {
        animateViewMoving(up: true, moveValue: 100)
    }
    
    func textFieldDidEndEditing(textField: UITextField) {
        animateViewMoving(up: false, moveValue: 100)
    }
    
    
    //Calls this function when the tap is recognized.
    func dismissKeyboard() {
        //Causes the view (or one of its embedded text fields) to resign the first responder status.
        view.endEditing(true)
    }
    
    // default view controller stuff
    override func viewDidLoad() {
        super.viewDidLoad()
        //UIRefreshControl.addTarget(self, action: #selector(refresh(_:)))
        self.popupView.isHidden = true
        self.errorView.isHidden = true
        self.popupView.layer.cornerRadius = 8.0
        self.errorView.layer.cornerRadius = 8.0
        if (self.getInProgress == false) {
            self.makeGETCall()
            self.getInProgress = true
        }
        //Looks for single or multiple taps.
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: "dismissKeyboard")
        tap.cancelsTouchesInView = false
        view.addGestureRecognizer(tap)
        
    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        print("view appeared")
        if (self.getInProgress == false) {
            print("making get call in viewDidAppear")
            self.makeGETCall()
            self.getInProgress = true
        }
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
        return self.totalNumItems
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = self.tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath) as? BuyPageCell
        if (image_data.count == self.totalNumItems && self.descriptions.count == self.totalNumItems && self.prices.count == self.totalNumItems && self.servings.count == self.totalNumItems) {
            popupView.isHidden = true
            cell?.photo.image = UIImage(data: image_data[indexPath.row])
            cell?.name.text = self.descriptions[indexPath.row]
            cell?.price.text = "Price: $" + String(self.prices[indexPath.row])
            cell?.servingsAvailable.text = "Servings: " + String(self.servings[indexPath.row])
            cell?.servingsBought.text = ""
            cell?.timeLeft.text = self.ends[indexPath.row]
        }
        return cell!
    }
    
    @IBAction func buyItemFinal(_ sender: Any) {
        let sellerid = self.userids[itemNumberBought]
        let buyerid = userid
        let jsonDict = ["sellerid": sellerid, "buyerid": buyerid, "servings": self.servingsBought] as [String : Any]
        self.makePOSTCall(jsonDict: jsonDict, api_route: "/api/v1/buy/", login: false)
    }
    
    func tableView(_ tableView: UITableView, willSelectRowAt indexPath: IndexPath) -> IndexPath? {
        let cell = tableView.cellForRow(at: indexPath) as! BuyPageCell
        if (cell.servingsBought.text != "") {
            popupView.isHidden = false
            itemNumberBought = indexPath.row
            self.servingsBought = Int(cell.servingsBought.text!)!
            print(indexPath.row)
            return indexPath
        } else {
            print("row selected with no input data")
            return nil
        }
    }
    
    @IBAction func errorConfirmation(_ sender: Any) {
        self.errorView.isHidden = true
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        //Change the selected background view of the cell.
        tableView.deselectRow(at: indexPath, animated: true)
        let cell = tableView.cellForRow(at: indexPath) as! BuyPageCell
        cell.servingsBought.text = ""
    }
}

