import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { Category } from 'src/app/models/category';
import { Story } from 'src/app/models/story';
import { AuthService } from 'src/app/services/auth.service';
import { StoryService } from 'src/app/services/story.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  categories: Category[] = [];
  stories: Story[] = [];
  page: number = 0;
  currentUserId: string = "";
  selectedFilter: string = "";

  constructor(private storyService: StoryService,
              private authService: AuthService) { }

    ngOnInit(): void {
      this.storyService.getCategories().subscribe(res => {
        console.log(res);
        this.categories = res['categories'];
      })

      this.storyService.getLatestStories(this.page).subscribe(res => {
        this.stories = res['stories'];
        console.log(res);
      })

      this.authService.getCurrentUser().subscribe(res => {
        this.currentUserId = res["id"];
      })
    }

    onClick() {
      this.page = this.page + 1;
      this.storyService.getLatestStories(this.page).subscribe(res => {
        // let tmp = new Array();
        // tmp = res['stories'];
        res['stories'].forEach((element: Story) => {
          this.stories.push(element);
        });
  
        console.log("Afrter",this.stories);
      })
    }


  filterByCategory(catId: string) {
    if(this.selectedFilter != catId) {
      this.selectedFilter = catId;
      this.storyService.getLatestStoriesByCategory(catId, this.page).subscribe(res => {
        this.stories = res['stories'];
      })
    } else if(this.selectedFilter == catId ){
      this.selectedFilter = "";
      this.storyService.getLatestStories(this.page).subscribe(res => {
        this.stories = res['stories'];
        console.log(res);
      })
    }
  }

  onStoryDeleted(storyId: string) {
    console.log("Story id breeeeej", storyId)
    this.storyService.deleteStory(storyId).subscribe(res => {
      console.log(res);

      this.storyService.getLatestStories(this.page).subscribe(res => {
        this.stories = res['stories'];
        console.log(res);
      })
    })

    
    
  }
}
