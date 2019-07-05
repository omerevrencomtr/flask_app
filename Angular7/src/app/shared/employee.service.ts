import { Injectable } from '@angular/core';
import { Employee } from './employee.model';
import { HttpClient } from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class EmployeeService {

  formData  : Employee;
  list : Employee[];
  readonly rootURL ="http://127.0.0.1:5000/api/v1"

  constructor(private http : HttpClient) { }

  postEmployee(formData : Employee){
   return this.http.post(this.rootURL+'/data',formData);

  }

  refreshList(){
    this.http.get(this.rootURL+'/data')
    .toPromise().then(res => this.list = res as Employee[]);
  }

  putEmployee(formData : Employee){
    return this.http.put(this.rootURL+'/data/'+formData.id,formData);
     
   }

   deleteEmployee(id : string){
    return this.http.delete(this.rootURL+'/data/'+id);
   }
}
