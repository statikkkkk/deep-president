import { Component } from '@angular/core';

import { QueryService } from './../services/query.service';
import { HttpClient } from '../services/httpclient.service';
import {Router} from '@angular/router';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'], 
  providers: [QueryService, HttpClient]
})
export class PendingComponent {

	current_text:string = "~"
	constructor(private queryService: QueryService, private router: Router){
    	this.check_val()
   }

check_val(){
      
          this.queryService.checkSpeech().subscribe(
            res => {
              console.log(res.words)
              if(this.current_text != "~" && res.words != this.current_text){
                this.router.navigateByUrl('/speech');
              }else{
                setTimeout(this.check_val(), 2000);
              }

              this.current_text = res.words
            },err => { 
              console.log(err)
              setTimeout(this.check_val(), 2000);
  
            })
}

}
