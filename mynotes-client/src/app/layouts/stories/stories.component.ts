import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Story } from 'src/app/models/story';
import { StoryService } from 'src/app/services/story.service';

@Component({
  selector: 'app-stories',
  templateUrl: './stories.component.html',
  styleUrls: ['./stories.component.css']
})
export class StoriesComponent {
  @Input('stories') stories: Story[] = [];
  @Input('currentUserId') currentUserId: string = "";
  @Output() storyDeleted: EventEmitter<any> = new EventEmitter();


  constructor(private storyService: StoryService) {}

  ngOnInit() {

  }
  
  onStoryDeleted(storyId: any) {
    this.storyDeleted.emit(storyId);
  }
}
