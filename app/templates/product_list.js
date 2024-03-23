function productList() {
    return {
        products: {{ products | tojson }},
        showModal: false,
        init() {
            this.listenForUpdates();
        },
        listenForUpdates() {
            const ws = new WebSocket('ws://localhost:8000/ws');
            ws.onmessage = (event) => {
                const productUpdate = JSON.parse(event.data);
                const index = this.products.findIndex((p) => p.id === productUpdate.id);
                if (index !== -1) {
                    this.products[index] = productUpdate;
                } else {
                    this.products.push(productUpdate);
                }
                this.products = this.products.slice(); // Trigger Alpine.js reactivity

                window.dispatchEvent(new CustomEvent('message-received', {
                    detail: 'Product updated successfully!'
                }));
            };
        }
    }
}