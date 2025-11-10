class CreateResourcePlannerCapacities < ActiveRecord::Migration[6.1]
  def change
    create_table :resource_planner_capacities, if_not_exists: true do |t|
      t.references :user, null: false, foreign_key: true, index: { unique: true }
      t.decimal :hours_per_week, precision: 5, scale: 2, null: false, default: 40.0

      t.timestamps
    end
  end
end

