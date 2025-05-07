# ActiveJob

ActiveJob is a framework in Ruby on Rails that provides a unified interface for background job processing. It allows developers to write job classes that can be executed asynchronously using various queuing backends like Sidekiq, Resque, or Delayed Job.

---

# When should you use ActiveJob?

ActiveJob should be used when you need to perform tasks asynchronously, such as sending emails, processing large datasets, or performing time-consuming operations that don’t need to block the main application flow.
