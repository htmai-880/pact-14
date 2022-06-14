package fr.pact14.s2r;

import java.util.List;

public class Ingredient {

    private String name;

    private String id;

    private List<String> label;

    //private String amount;

    private String category;

    private String subCategory;


    private IngredientProperties properties;

    public Ingredient(String name, String category, String subCategory, IngredientProperties properties) {
        this.name = name;
        this.category = category;
        this.subCategory = subCategory;
        this.properties = properties;
    }

    public String getName() {
        return name;
    }

    public String getCategory() {
        return category;
    }

    public String getSubCategory() {
        return subCategory;
    }

    public String getId() {
        return id;
    }

    public List<String> getLabel() {
        return label;
    }

    public IngredientProperties getProperties() {
        return properties;
    }

    public static class IngredientProperties {
        private int quantity_denominator;
        private int quantity_numerator;
        private String unit;
        private String prep;

        public int getQuantity_denominator() {
            return quantity_denominator;
        }

        public int getQuantity_numerator() {
            return quantity_numerator;
        }

        public String getUnit() {
            return unit;
        }

        public String getPrep(){
            return prep;
        }

        public IngredientProperties(int quantity_denominator, int quantity_numerator, String unit, String prep) {
            this.quantity_denominator = quantity_denominator;
            this.quantity_numerator = quantity_numerator;
            this.unit = unit;
            this.prep = prep;
        }
    }
}
