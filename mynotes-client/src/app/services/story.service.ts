import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Story } from '../models/story';

@Injectable({
  providedIn: 'root'
})
export class StoryService {
  serverUrl:string = "http://127.0.0.1:5000/";

  constructor(private http: HttpClient) { }

  getStory(storyId: String) {
    let params = new HttpParams().set("id", storyId.toString());
    return this.http.get<any>(this.serverUrl + "story/get-story", {params:params});
  }
  createStory(story: any) {
    return this.http.post(this.serverUrl + 'story/create-story', story);
  }

  getCategories() {
    return this.http.get<any>(this.serverUrl + "story/get-categories");
  }

  getLatestStories(page: Number) {
    let params = new HttpParams().set("page", page.toString());
    return this.http.get<any>(this.serverUrl + "story/get-latest-stories", {params:params});
  }

  getLatestStoriesByCategory(catId:string, page: Number) {
    let params = new HttpParams().set("page", page.toString()).set("categoryId", catId);
    return this.http.get<any>(this.serverUrl + "story/get-latest-by-cat", {params:params});
  }

  updateStory(story: Story) {
    return this.http.patch(this.serverUrl + 'story/update-story', story);
  }

  deleteStory(storyId: string) {
    let params = new HttpParams().set("id", storyId.toString());
    return this.http.delete<any>(this.serverUrl + 'story/delete-story', {params:params});
  }
}
