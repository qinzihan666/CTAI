update(e) {
    console.log("Update method called");
    const file = e.target.files[0];
    console.log("Selected file:", file);
    
    if (!file) {
        console.log("No file selected");
        return;
    }
    
    this.loading = true;
    console.log("Loading state set to true");
    
    const formData = new FormData();
    formData.append('file', file);
    console.log("FormData created with file");
    
    axios.post('/upload', formData)
        .then(response => {
            console.log("Upload response:", response.data);
            this.loading = false;
            this.imageUrl = response.data.url;
            this.maskUrl = response.data.mask_url;
            this.drawUrl = response.data.draw_url;
            console.log("Image URLs updated:", {
                imageUrl: this.imageUrl,
                maskUrl: this.maskUrl,
                drawUrl: this.drawUrl
            });
        })
        .catch(error => {
            console.error("Upload error:", error);
            this.loading = false;
        });
} 