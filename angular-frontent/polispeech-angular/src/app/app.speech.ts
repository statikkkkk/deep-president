import { Component } from '@angular/core';
import {QueryService} from './../services/query.service';
import { HttpClient } from '../services/httpclient.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.speech.html',
  styleUrls: ['./app.component.css'], 
  providers: [QueryService, HttpClient]
})

export class SpeechComponent {

  constructor(private queryService: QueryService){
      this.check_val()
   }

   words: string[] = []
   polarity:any = {}
   type:number = 1
   get_color(){

   }
check_val(){
      

          this.queryService.checkSpeech().subscribe(
            res => {         
              this.words = res.words.split(" ");
              this.polarity = res.word_polarity
            },err => { 
              console.log(err)
              setTimeout(this.check_val(), 2000);
  
            })
}

}
