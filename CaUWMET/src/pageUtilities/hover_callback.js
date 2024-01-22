// This script configures the hover callback for bokeh
// So when a user hovers over points on the graph, the size/alpha changes
var data = source.data;
var indices = cb_data.index.indices;
var alpha = data['alpha'];
var originalAlpha = data['original_alpha'];
var size = data['size'];
var originalSize = data['original_size'];

// Initialize originalAlpha if not already present
if (!originalAlpha) {
    data['original_alpha'] = alpha.slice();
    originalAlpha = data['original_alpha'];
}

// Reset alpha to original for all circles
for (var i = 0; i < alpha.length; i++) {
    alpha[i] = originalAlpha[i];
}

// Initialize originalSize if not already present
if (!originalSize) {
    data['original_size'] = size.slice(); 
    originalSize = data['original_size'];
}

// Reset size to original for all circles
for (var i = 0; i < size.length; i++) {
    size[i] = originalSize[i];
}

// Set alpha to 1 and size x2 for the top-most hovered circle
if (indices.length > 0) {
    alpha[indices[0]] = 1.0;
    size[indices[0]] = originalSize[indices[0]] * 2;
}

// Update the source data
source.change.emit();