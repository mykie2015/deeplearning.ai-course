
## Sora process

``` PlantUML
@startuml
!theme plain

participant User
participant "Sora AI" as Sora
database "Video & Text Data" as Data

User -> Sora : Text Prompt\n(e.g., "A dog chasing a butterfly in a sunny park.")
Sora -> Data : Searches & Analyzes Data
Data -> Sora : Provides Matching Clips

group Video Generation
    Sora -> Sora : Identifies Key Elements & Actions
    Sora -> Sora : Scene Breakdown
    Sora -> Sora : Visual Search & Smart Selection
    Sora -> Sora : Seamless Transitions\n(Crossfades, Color Correction)
    Sora -> Sora : Creative Touches\n(Simulated Camera Movement, Stylization)
end

group Emulating Physics
    Sora -> Sora : Learning from Real World Physics
    Sora -> Sora : Uses Internal Physics Engine\n(For Realistic Movement & Interactions)
    Sora -> Sora : Fine-tuning for Visual Realism
end

Sora -> User : Generates & Presents Video

note right of Sora
  Sora is experimental and
  showcases the potential of
  text-to-video AI.
end note

note left of Data
  Sora's capabilities depend on
  the quality and diversity of
  its training data.
end note

@enduml


```
