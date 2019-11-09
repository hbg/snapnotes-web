//
//  ViewController.swift
//  SnapNotes
//
//  Created by james luo on 11/9/19.
//  Copyright © 2019 james luo. All rights reserved.
//

import UIKit
import FirebaseMLVision
import FirebaseDatabase
class ViewController: UIViewController,UIImagePickerControllerDelegate,UINavigationControllerDelegate {
var curClass = ""
   let ref = Database.database().reference()
    @IBOutlet weak var myImage: UIImageView!
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    @IBAction func parseImage(_ sender: Any) {
        parseData()
    }
    
    @IBAction func TakePhoto(_ sender: Any) {
        loadCam()
    }
    func loadCam(){
        if UIImagePickerController.isSourceTypeAvailable(.camera) {
            let imagePickerController = UIImagePickerController()
            imagePickerController.delegate = self;
            imagePickerController.sourceType = .camera
            self.present(imagePickerController, animated: true, completion: nil)
            
            
        }
        
           
    }
    func parseData(){
        let vision = Vision.vision()
        let textRecognizer = vision.cloudTextRecognizer()
        if let foundImage = myImage.image{
            let imageVision = VisionImage(image: foundImage)
            textRecognizer.process(imageVision) { result, error in


              // Text recognition results
                if let resultText = result?.text{
                    let sentence = resultText
                    let lines = sentence.split { $0.isNewline }
                    var ContentStr = ""
                    let limit = lines.count - 1
                    for i in (1 ... limit ){
                        ContentStr = ContentStr + lines[i] + "\n"
                    }
                    self.ref.child("courses/" + self.curClass + "/"+String(lines[0])).setValue(ContentStr)
                    print(lines)   // "[Line 1, Line 2, Line 3]"
                }
                
                
                        // `VisionText` is made of `VisionTextBlock`s...

            }

        }
    }
    
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        let image = info[UIImagePickerController.InfoKey.originalImage] as? UIImage
        myImage.image = image
        self.dismiss(animated: true, completion: nil)
    }
    

}

