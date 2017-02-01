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
    
    var names = ["Enchilada", "Cheesecake", "Wings"]
    var images = [UIImage(named: "enchilada"), UIImage(named: "cheesecake"), UIImage(named: "wings")]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        popupView.isHidden = true
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    @IBAction func buyItem(_ sender: UIButton) {
        
        popupView.isHidden = false
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 2
    }
    
    @IBAction func cancelPopup(_ sender: Any) {
        popupView.isHidden = true
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = self.tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath) as! BuyPageCell
        cell.photo.image = images[indexPath.row]
        cell.name.text = names[indexPath.row]
        return cell
    }
}

