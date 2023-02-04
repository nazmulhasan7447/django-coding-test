import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import TagsInput from "react-tagsinput";
import "react-tagsinput/react-tagsinput.css";
import Dropzone from "react-dropzone";
import Axios from "axios";
import { size } from "lodash";
import { data } from "jquery";

Axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
Axios.defaults.xsrfCookieName = "csrftoken";

const EditProduct = (props) => {
  const location = window.location.pathname;
  const [showAlertMessage, setShowAlertMessage] = useState({
    show: false,
    status: "",
  });
  const [productVariantPrices, setProductVariantPrices] = useState([]);
  const [productInfo, setProductInfo] = useState({});

  //   console.log(productVariantPrices);

  //   console.log(productInfo);

  const [productVariants, setProductVariant] = useState([
    {
      option: 1,
      tags: [],
    },
  ]);

  // handle click event of the Add button
  const handleAddClick = () => {
    let all_variants = JSON.parse(props.variants.replaceAll("'", '"')).map(
      (el) => el.id
    );
    let selected_variants = productVariants.map((el) => el.option);
    let available_variants = all_variants.filter(
      (entry1) => !selected_variants.some((entry2) => entry1 == entry2)
    );
    setProductVariant([
      ...productVariants,
      {
        option: available_variants[0],
        tags: [],
      },
    ]);
  };

  // handle input change on tag input
  const handleInputTagOnChange = (value, index) => {
    let product_variants = [...productVariants];
    product_variants[index].tags = value;
    setProductVariant(product_variants);

    checkVariant();
  };

  // remove product variant
  const removeProductVariant = (index) => {
    let product_variants = [...productVariants];
    product_variants.splice(index, 1);
    setProductVariant(product_variants);
  };

  // check the variant and render all the combination
  const checkVariant = () => {
    let tags = [];

    productVariants.filter((item) => {
      tags.push(item.tags);
    });

    setProductVariantPrices([]);

    getCombn(tags).forEach((item, index) => {
      setProductVariantPrices((productVariantPrice) => [
        ...productVariantPrice,
        {
          index,
          title: item,
          price: 0,
          stock: 0,
        },
      ]);
      setProductInfo({
        ...productInfo,
        variants: [
          ...productVariantPrices,
          {
            index,
            variant_title: item,
            price: 0,
            stock: 0,
          },
        ],
      });
    });
  };

  const varientHandler = (e, id) => {
    if (
      e.target.name !== "product_name" ||
      e.target.name !== "product_sku" ||
      e.target.name !== "product_description"
    ) {
      setProductVariantPrices([
        ...productVariantPrices?.filter((item) => item?.id !== id),
        {
          ...productVariantPrices?.filter((item) => item?.id === id)[0],
          [e.target.name]: e.target.value,
        },
      ]);
      setProductInfo({
        ...productInfo,
        variants: [
          ...productVariantPrices?.filter((item) => item?.id !== id),
          {
            ...productVariantPrices?.filter((item) => item?.id === id)[0],
            [e.target.name]: e.target.value,
          },
        ],
      });
    }

    if (
      e.target.name === "product_name" ||
      e.target.name === "product_sku" ||
      e.target.name === "product_description"
    ) {
      setProductInfo({
        ...productInfo,
        [e.target.name]: e.target.value,
      });
    }
    // console.log(productInfo);
  };

  // combination algorithm
  function getCombn(arr, pre) {
    pre = pre || "";
    if (!arr.length) {
      return pre;
    }
    let ans = arr[0].reduce(function (ans, value) {
      return ans.concat(getCombn(arr.slice(1), pre + value + "/"));
    }, []);
    return ans;
  }

  const hanldeProductInfoChange = (e) => {
    setProductInfo({ ...productInfo, [e.target.name]: e.target.value });
  };

  useEffect(() => {
    Axios.get(`${location}product`)
      .then((response) => {
        // console.log(response);
        if (response?.data) {
          setProductInfo({
            ...productInfo,
            ...response?.data?.product,
            variants: response?.data?.product_varients,
          });
          setProductVariantPrices(response?.data?.product_varients);
        }
      })
      .then((error) => {
        console.log(error);
      });
  }, []);

  // Save product
  let saveProduct = (event) => {
    event.preventDefault();
    console.log(productInfo);
    console.log(productVariantPrices);
    // TODO : write your code here to save the product
    Axios.post(`${location}product/`, {
      ...productInfo,
      variants: productVariantPrices,
    })
      .then((response) => {
        console.log(response);
        if (response?.data === "success") {
          setShowAlertMessage({
            ...showAlertMessage,
            show: true,
            status: "success",
          });
        }
        if (response?.data === "Something went wrong") {
          setShowAlertMessage({
            ...showAlertMessage,
            show: true,
            status: "warning",
          });
        }
      })
      .then((error) => {
        if (response?.data === "Something went wrong") {
          setShowAlertMessage({
            ...showAlertMessage,
            show: true,
            status: "warning",
          });
        }
        // console.log(error);
      });
  };

  return (
    <div>
      <section>
        {showAlertMessage?.show && showAlertMessage?.status === "success" ? (
          <div className="row">
            <div className="col-12">
              <div
                class="alert alert-success alert-dismissible fade show"
                role="alert"
              >
                <strong>New product has been added successfully!</strong>
                <button
                  type="button"
                  class="close"
                  data-dismiss="alert"
                  aria-label="Close"
                >
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
            </div>
          </div>
        ) : showAlertMessage?.show && showAlertMessage?.status === "warning" ? (
          <div className="row">
            <div className="col-12">
              <div
                class="alert alert-danger alert-dismissible fade show"
                role="alert"
              >
                <strong>Something went wrong!</strong>
                <button
                  type="button"
                  class="close"
                  data-dismiss="alert"
                  aria-label="Close"
                >
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
            </div>
          </div>
        ) : (
          ""
        )}

        <div className="row">
          <div className="col-md-6">
            <div className="card shadow mb-4">
              <div className="card-body">
                <div className="form-group">
                  <label htmlFor="">Product Name</label>
                  <input
                    type="text"
                    placeholder="Product Name"
                    className="form-control"
                    name="title"
                    value={productInfo?.title}
                    onChange={hanldeProductInfoChange}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="">Product SKU</label>
                  <input
                    type="text"
                    placeholder="Product SKU"
                    className="form-control"
                    name="sku"
                    value={productInfo?.sku}
                    onChange={hanldeProductInfoChange}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="">Description</label>
                  <textarea
                    id=""
                    cols="30"
                    rows="4"
                    className="form-control"
                    name="description"
                    onChange={hanldeProductInfoChange}
                    value={productInfo?.description}
                  ></textarea>
                </div>
              </div>
            </div>

            <div className="card shadow mb-4">
              <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                <h6 className="m-0 font-weight-bold text-primary">Media</h6>
              </div>
              <div className="card-body border">
                <Dropzone
                  onDrop={(acceptedFiles) =>
                    setProductInfo({
                      ...productInfo,
                      product_img: acceptedFiles[0],
                    })
                  }
                >
                  {({ getRootProps, getInputProps }) => (
                    <section>
                      <div {...getRootProps()}>
                        <input {...getInputProps()} />
                        <p>
                          Drag 'n' drop some files here, or click to select
                          files
                        </p>
                      </div>
                    </section>
                  )}
                </Dropzone>
              </div>
            </div>
          </div>

          <div className="col-md-6">
            <div className="card shadow mb-4">
              <div className="card-header text-uppercase">Product Variants</div>
              <div className="card-body">
                <div className="table-responsive">
                  <table className="table">
                    <thead>
                      <tr>
                        <td>Variant</td>
                        <td>Price</td>
                        <td>Stock</td>
                      </tr>
                    </thead>
                    <tbody>
                      {productVariantPrices.map(
                        (productVariantPrice, index) => {
                          return (
                            <tr key={productVariantPrice?.id}>
                              <td>{productVariantPrice.variant_title}</td>
                              <td>
                                <input
                                  className="form-control"
                                  name="price"
                                  onChange={(e) => {
                                    varientHandler(e, productVariantPrice?.id);
                                  }}
                                  type="text"
                                  value={productVariantPrice?.price}
                                />
                              </td>
                              <td>
                                <input
                                  className="form-control"
                                  type="text"
                                  name="stock"
                                  value={productVariantPrice?.stock}
                                  onChange={(e) =>
                                    varientHandler(e, productVariantPrice?.id)
                                  }
                                />
                              </td>
                            </tr>
                          );
                        }
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button
          type="button"
          onClick={saveProduct}
          className="btn btn-lg btn-primary"
        >
          Save
        </button>
        <button type="button" className="btn btn-secondary btn-lg">
          Cancel
        </button>
      </section>
    </div>
  );
};

export default EditProduct;
