import React from "react";
import ReactDOM from "react-dom";
import CreateProduct from "./components/CreateProduct";
import EditProduct from "./components/EditProduct";
import { Routes, Route } from "react-router-dom";
// require('./bootstrap');
// require('./sb-admin');

const propsContainer = document.getElementById("variants");
const props = Object.assign({}, propsContainer.dataset);

// for edit product
// const currentProductInfo = document.getElementById("current_product");
// const currentProductInfoProps = Object.assign({}, currentProductInfo?.dataset);

const Index = () => {
  const location = window.location.pathname;
  console.log(location);

  return (
    <>
      {location === "/product/create/" && <CreateProduct {...props} />}

      {(location === "/product/update/" ||
        location?.split("/")?.includes("update")) && <EditProduct {...props} />}
    </>
  );
};

export default Index;
