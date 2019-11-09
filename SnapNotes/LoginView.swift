//
//  LoginView.swift
//  SnapNotes
//
//  Created by james luo on 11/9/19.
//  Copyright © 2019 james luo. All rights reserved.
//

import UIKit

class LoginView: UIViewController ,UITextFieldDelegate{
    var curClassID = ""
    override func viewDidLoad() {
        super.viewDidLoad()
        ClassID.delegate = self
        // Do any additional setup after loading the view.
    }
    
    @IBOutlet weak var ClassID: UITextField!
    @IBAction func login(_ sender: Any) {
        self.performSegue(withIdentifier: "toCapture", sender: self)
    }
    func textFieldDidBeginEditing(_ textField: UITextField) {
        ClassID.text = ""
        ClassID.becomeFirstResponder()
    }
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        curClassID = ClassID.text ?? "none"
        ClassID.resignFirstResponder()
        return true
    }
    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "toCapture"{
            if let nextView = segue.destination as? ViewController{
                nextView.curClass = curClassID
            }
        }
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    

}
