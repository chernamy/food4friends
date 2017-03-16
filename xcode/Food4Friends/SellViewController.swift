
//
//  SellController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 2/7/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

//
//  SellViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 2/12/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit

class Singleton {
    static let sharedInstance = Singleton()
    var imageValue : UIImage?
}

class SellViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    @IBOutlet weak var foodImage: UIImageView!
    @IBAction func openCamera(_ sender: Any) {
        
        let imagePicker = UIImagePickerController()
        
        imagePicker.delegate = self
        imagePicker.sourceType = UIImagePickerControllerSourceType.camera
        imagePicker.allowsEditing = false
        
        
        self.present(imagePicker, animated: true,
                     completion: nil)
        
    }
    
    @IBAction func openPhotoLibrary(_ sender: Any) {
        if UIImagePickerController.isSourceTypeAvailable(
            UIImagePickerControllerSourceType.savedPhotosAlbum) {
            let imagePicker = UIImagePickerController()
            
            imagePicker.delegate = self
            imagePicker.sourceType =
                UIImagePickerControllerSourceType.photoLibrary
            imagePicker.allowsEditing = false
            self.present(imagePicker, animated: true,
                         completion: nil)
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        
        let image = info[UIImagePickerControllerOriginalImage] as! UIImage
        foodImage.image = image
        Singleton.sharedInstance.imageValue = image
        self.dismiss(animated: true, completion: nil)
    }
    
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        self.dismiss(animated: true, completion: nil)
    }
    
}




