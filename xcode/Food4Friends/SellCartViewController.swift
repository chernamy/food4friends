//
//  SellCartViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 3/15/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit


class SellCartViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
    
    @IBOutlet weak var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.delegate = self;
        tableView.dataSource = self;
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // For creating the table view
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // return how many rows in the table
        return 3
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let cell = self.tableView.dequeueReusableCell(withIdentifier: "sellCell", for: indexPath) as! SellCartCell
        cell.servings?.text = "servings: 3"
        cell.buyerImage?.image = #imageLiteral(resourceName: "enchilada")
        return cell
    }

}
