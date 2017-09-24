import { Component } from '@angular/core';

import { QueryService } from './../services/query.service';
import { HttpClient } from '../services/httpclient.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'], 
  providers: [QueryService, HttpClient]
})
export class PendingComponent {

	current_text:string = ""
	constructor(private queryService: QueryService){
    	this.check_val()
   }

check_val(){
      


          this.queryService.checkSpeech().subscribe(
            res => {
              if(this.current_text != "" && res.text() != this.current_text){
                console.log("UPDATED STRINGGGG")
              }else{
                this.check_val()
              }

              this.current_text = res.text()
            },err => { 
              console.log(err)
              this.check_val()
            })
       
    
  

}

}
