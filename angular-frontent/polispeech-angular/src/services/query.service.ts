import {Injectable} from '@angular/core'
import {Response} from '@angular/http'
import { config } from '../app.config'
import { HttpClient } from './httpclient.service';
import 'rxjs/add/operator/map'

@Injectable()
export class QueryService{
	constructor(private http: HttpClient){}
	checkSpeech(){
		return this.http.get(config.URI+'/generate_republican_sentence').map(res => res);
	}
}