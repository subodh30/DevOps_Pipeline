const request = require("supertest");
const chai = require("chai");
const app = require("../../app");

const expect = chai.expect;

describe("Coffee Delivery Service API", () => {
  describe("POST /order and GET /orders", () => {
    it("should place an order and retrieve it in the list of orders", (done) => {
      request(app)
        .post("/order")
        .send({ coffeeId: 1, quantity: 1 })
        .end((err, res) => {
          expect(res.statusCode).to.equal(201);
          const orderId = res.body.orderId;

          // Retrieve the list of orders and check if the order is there
          request(app)
            .get("/orders")
            .end((err, res) => {
              expect(res.statusCode).to.equal(200);
              expect(res.body).to.be.an("array");

              // Check if the order with the placed orderId exists in the list
              const placedOrder = res.body.find(
                (order) => order.orderId === orderId
              );
              expect(placedOrder).to.exist;
              expect(placedOrder.coffeeName).to.equal("Latte");
              expect(placedOrder.quantity).to.equal(1);
              expect(placedOrder.total).to.equal(5);
              done();
            });
        });
    });
  });
});
