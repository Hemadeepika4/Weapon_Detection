import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  baseUrl = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  signup(data: any) {
    return this.http.post(`${this.baseUrl}/signup`, data);
  }

  login(data: any) {
    return this.http.post(`${this.baseUrl}/login`, data);
  }

  getUploads(userId: number) {
    return this.http.get(`${this.baseUrl}/uploads/${userId}`);
  }

  detectImage(formData: FormData) {
    return this.http.post(`${this.baseUrl}/detect-image`, formData);
  }

  detectVideo(formData: FormData) {
    return this.http.post(`${this.baseUrl}/detect-video`, formData);
  }
}