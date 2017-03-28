

//
//  SellCartCell.swift
//  Food4Friends
//
//  Created by Vaish Raman on 3/18/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit

class SellCartCell: UITableViewCell {

    @IBOutlet weak var buyerImage: UIImageView!
    @IBOutlet weak var buyerName: UILabel!
    @IBOutlet weak var servings: UILabel!
    @IBOutlet weak var transactionCompleted: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
        self.buyerImage.layer.cornerRadius = self.buyerImage.frame.size.width / 2
        self.buyerImage.clipsToBounds = true
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure sthe view for the selected state
    }

}
