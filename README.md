## What is a WMC (White Matter Classification) object _conceptually_?

A WMC is best thought of as the tractogram's equivalent of a parcellation for a nifti brain volume, in that it assigns (anatomical) identities to the constituent elements (in this case streamlines) of the larger object.  It is the result of the interaction of the following three entities:

1. A tractogram:  a specific, omnibus, streamline-based, heterogenous (in that it does not correspond to one indifferentiable "thing") model of white matter anatomy.
2.  A white matter ontology:  a finite set of white matter anatomical entities to which the constituent streamlines of the associated tractogram can be assigned membership.
3.  A segmentation:  a ruleset or algorithm that is used to assign the constituent elements of the tractogram (i.e., streamlines) membership or identity amongst the elements of the associated white matter ontology.  

In this way, a given WMC object is a-contextual (and thus relatively uninterpretable) _unless_ it can be clearly and easily associated with the _specific instances_ of the three entities listed above.

Furthermore, there are distinct goals and assessment criteria for each of these three entities, and each can fail in distinct ways, each of which would result in the manifestation of errors in the downstream WMC object.  See the figure below for a diagrammatic illustration of how failures in sensitivity and specificity for these objects would manifest.

![WMC component diagram](https://raw.githubusercontent.com/DanNBullock/WiMSE/master/images/SensitivitySpecificitySchema.png)

## What is a WMC (White Matter Classification) object _structurally_?

In essence, the WMC is composed of two parts:  **the index vector** and **the names vector**.

### .index
The index vector is a 1 by n vector of integers assigning categorical identity/membership to the streamlines of **the associated tck entity** (tractogram), where n is the number of streamlines in the tck object.  The integer values assigned to each streamline correspond to the index of a name in the name field, which itself corresponds to an element of the associated white matter ontological set.  **The index vector is not zero indexed** , meaning that an entry of zero **does not** correspond to the first entry on the names list.  Instead, a streamline with 0 in its .index entry indicates that no _specific_ identity was assigned to this streamline.  This is perfectly permissible and may result from one of several causes (with respect to the diagram above, a failure for one of the following scenarios to obtain:  "No 'false positive' streamlines", "all WM entities enumerated", or "all streamlines mapped").  Indeed, an ontology that intends to leave no component of the white matter uncategorized can be described as _complete_ (i.e. https://doi.org/10.25663/brainlife.app.249), while one that does not have this intent can be described as _incomplete_ (https://doi.org/10.25663/brainlife.app.188 or https://doi.org/10.25663/brainlife.app.207)

As it is currently implemented, the WMC, _as a data construct_ (and thus any given instance of a WMC), is both _exclusive_ and _non-hierarchical_.  This means that for any streamline, for a given WMC object, there can be _only one_ white matter anatomical entity/category (i.e., name) that it can be assigned to, and that (**generally speaking**) there is no higher order structuring of entities/categories _with respect to the structure of the WMC object itself_.  This stipulation warrants a couple of qualifications, though.  In practice, it is best to keep the right and left variants of an anatomical entity (should they exist) next to one another in the .names field (and thus also in .index numeration) for the sake of interpretability.  Furthermore, while there may be hierarchical structure within the associated white matter ontology _itself_, that could potentially be inferred from naming conventions in the .names field, there is nothing inherent to the WMC structure _itself_ that would or could indicate this.

### .names
The .names vector enumerates those anatomical structures (ontological set members of the associated white matter ontology superset) for which _at least one streamline_ has been mapped in the associated tractogram.  _It is NOT an exhaustive list of the superset composed by the complete associated white matter ontology, but rather the subset of these which have been segmented from the associated tractogram_ .  For practical reasons (e.g., brevity), these entires may be abbreviations or shortened versions of longer category labels/names from the associated white matter ontology.  

## Quick rules

- No spaces in .names entries:  default replacement behavior should be to replace spaces with underscores
- Some but not all .name entries will correspond to the "left" or "right" right variant of a category/structure.  Such paired entires should be kept next to each other, and the associated .index values should be adjusted accordingly (see https://github.com/DanNBullock/wma_tools/blob/master/ClassificationStruc_Tools/wma_resortClassificationStruc.m for an example implementation).
-  All .names entries should be unique
-  No entries in the .name list may be blank (a blank entry could not correspond to category from the associated white matter ontology)
- Under **no circumstance** should the length of unique entries in .index exceed the number of entries in .names **except** in the case that some streamlines have not been assigned an explicit identity (i.e., "name") and have thus been assigned a numerical identity of 0, which does not correspond to an entry in .names (and so, in such a case length(unique(classification.index))+1==length(unique(classification.names))).
-  Conversely, the length of the .names vector should be equal to length(unique(classification.index)), keeping the above provision in mind.  (_perhaps this point could be up for debate, but we should keep in mind the downstream consequences of such a decision_)
- Because no name entries may be blank, and because all entities in the .names field must have _at least one_ exemplar streamline (open to debate), the numbering sequence used in the .index vector should be contiguously sequenced (i.e., 1:1:n, no skipping numbers)
- The number of entries in the .index vector should be **EXACTLY EQUAL** to the number of streamlines in the associated tractogram.
-  Because the identities assigned in the WMC object are locked to specific streamlines in the source tractogram, the sequencing of entries in the .index vector should be kept locked to the sequence of streamlines.  That is, if the sequential ordering of the streamlines in the associated tractogram (/.tck object) changes, the ordering of the corresponding WMC objects should change in exact correspondence with this shift.  Given that multiple WMC objects (from multiple ontologies/segmentations) could be associated with a single tractogram, **the sequencing of the source tractogram should take precedence over any particular WMC object**.
-   For the above reason, you should essentially **never* change the ordering of streamlines in a tractogram (e.g., .tck) object.
