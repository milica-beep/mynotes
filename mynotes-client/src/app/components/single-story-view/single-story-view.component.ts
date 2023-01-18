import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Story } from 'src/app/models/story';
import { StoryService } from 'src/app/services/story.service';

@Component({
  selector: 'app-single-story-view',
  templateUrl: './single-story-view.component.html',
  styleUrls: ['./single-story-view.component.css']
})
export class SingleStoryViewComponent {
  @Input('story') story: Story = new Story;
  @Input('currentUserId') currentUserId: string = "";
  @Output() storyDeleted: EventEmitter<any> = new EventEmitter();

  constructor(private storyService: StoryService) {}

  ngOnInit() {

  }

  onDelete() {
    // this.storyService.deleteStory(this.story.id).subscribe(res => {
    //   console.log(res);
    // })

    this.storyDeleted.emit(this.story.id);
  }

}
