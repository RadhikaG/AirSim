// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

#ifndef airsim_core_PhysicsBody_hpp
#define airsim_core_PhysicsBody_hpp

#include "Battery.hpp"
#include "common/Common.hpp"
#include "common/UpdatableObject.hpp"
#include "PhysicsBodyVertex.hpp"
#include "common/CommonStructs.hpp"
#include "Kinematics.hpp"
#include "Environment.hpp"
#include <unordered_set>
#include <exception>
namespace msr { namespace airlib {

class PhysicsBody : public UpdatableObject {
public: //interface
    virtual void kinematicsUpdated() = 0;
    virtual real_T getRestitution() const = 0;
    virtual real_T getFriction() const = 0;

    //derived class may return covariant type
    virtual uint wrenchVertexCount() const
    {
        return 0;
    }
    virtual PhysicsBodyVertex& getWrenchVertex(uint index)
    {
        unused(index);
        throw std::out_of_range("no physics vertex are available");
    }
    virtual const PhysicsBodyVertex& getWrenchVertex(uint index) const
    {
        unused(index);
        throw std::out_of_range("no physics vertex are available");
    }

    virtual uint dragVertexCount() const
    {
        return 0;
    }
    virtual PhysicsBodyVertex& getDragVertex(uint index)
    {
        unused(index);
        throw std::out_of_range("no physics vertex are available");
    }
    virtual const PhysicsBodyVertex& getDragVertex(uint index) const
    {
        unused(index);
        throw std::out_of_range("no physics vertex are available");
    }
    virtual void setCollisionInfo(const CollisionInfo& collision_info)
    {
        collision_info_ = collision_info;
    }

public: //methods
    //constructors
    PhysicsBody()
    {
        //allow default constructor with later call for initialize
    }
    PhysicsBody(real_T mass, const Matrix3x3r& inertia, const Kinematics::State& initial_kinematic_state, Environment* environment)
    {
        initialize(mass, inertia, initial_kinematic_state, environment);
    }
    void initialize(real_T mass, const Matrix3x3r& inertia, const Kinematics::State& initial_kinematic_state, Environment* environment)
    {
        kinematics_.initialize(initial_kinematic_state);

        mass_ = mass;
        mass_inv_ = 1.0f / mass;
        inertia_ = inertia;
        inertia_inv_ = inertia_.inverse();
        environment_ = environment;
    }

    //enable physics body detection
    virtual UpdatableObject* getPhysicsBody() override
    {
        return this;
    }


    //*** Start: UpdatableState implementation ***//
    virtual void reset() override
    {
        UpdatableObject::reset();

        kinematics_.reset();

        if (environment_)
            environment_->reset();
        wrench_ = Wrench::zero();
        collision_info_ = CollisionInfo();
        collision_response_info_ = CollisionResponseInfo();

        //update individual vertices
        for (uint vertex_index = 0; vertex_index < wrenchVertexCount(); ++vertex_index) {
            getWrenchVertex(vertex_index).reset();
        }
        for (uint vertex_index = 0; vertex_index < dragVertexCount(); ++vertex_index) {
            getDragVertex(vertex_index).reset();
        }
    }

	virtual void updateTime(TTimeDelta dt) {
		total_time_since_creation_ += dt;
	}
	virtual void updateDistanceTraveled(Pose cur_pose) {
		if (distance_traveled_ == -1) { //first value
			distance_traveled_ = 0;
			last_pose_ = cur_pose;
		}
		
		double distance_traveled_temp = sqrt(pow((cur_pose.position - last_pose_.position)[0],2) + pow((cur_pose.position - last_pose_.position)[1],2) + pow((cur_pose.position - last_pose_.position)[2],2));
		
		if (distance_traveled_temp > distance_traveled_quanta_) { //only update if greater than certain threshold cause otherwise the error accumulates
			distance_traveled_ += distance_traveled_temp;
			last_pose_ = cur_pose;
		}
	}
   
	virtual void updateEnergyConsumed(double inst_energy) {
		energy_consumed_ += inst_energy;
	}


    virtual void update() override
    {
        UpdatableObject::update();

        //update position from kinematics so we have latest position after physics update
        environment_->setPosition(getKinematics().pose.position);
        environment_->update();

        kinematics_.update();

        //update individual vertices
        for (uint vertex_index = 0; vertex_index < wrenchVertexCount(); ++vertex_index) {
            getWrenchVertex(vertex_index).update();
        }
        for (uint vertex_index = 0; vertex_index < dragVertexCount(); ++vertex_index) {
            getDragVertex(vertex_index).update();
        }
    }

    virtual void reportState(StateReporter& reporter) override
    {
        //call base
        UpdatableObject::reportState(reporter);

        reporter.writeHeading("Kinematics");
        kinematics_.reportState(reporter);
    }
    //*** End: UpdatableState implementation ***//


    //getters
    real_T getMass()  const
    {
        return mass_;
    }
    real_T getMassInv()  const
    {
        return mass_inv_;
    }
    const Matrix3x3r& getInertia()  const
    {
        return inertia_;
    }
    const Matrix3x3r& getInertiaInv()  const
    {
        return inertia_inv_;
    }

    const Pose& getPose() const
    {
        return kinematics_.getPose();
    }
    void setPose(const Pose& pose)
    {
        return kinematics_.setPose(pose);
    }
    const Twist& getTwist() const
    {
        return kinematics_.getTwist();
    }
    void setTwist(const Twist& twist)
    {
        return kinematics_.setTwist(twist);
    }


    const Kinematics::State& getKinematics() const
    {
        return kinematics_.getState();
    }
    void setKinematics(const Kinematics::State& state)
    {
        if (VectorMath::hasNan(state.twist.linear)) {
            //Utils::DebugBreak();
            Utils::log("Linear velocity had NaN!", Utils::kLogLevelError);
        }

        kinematics_.setState(state);
    }
    const Kinematics::State& getInitialKinematics() const
    {
        return kinematics_.getInitialState();
    }
    const Environment& getEnvironment() const
    {
        return *environment_;
    }
    Environment& getEnvironment()
    {
        return *environment_;
    }
    bool hasEnvironment() const
    {
        return environment_ != nullptr;
    }
    const Wrench& getWrench() const
    {
        return wrench_;
    }
    void setWrench(const Wrench&  wrench)
    {
        wrench_ = wrench;
    }
    const CollisionInfo& getCollisionInfo() const
    {
        return collision_info_;
    }

    const CollisionResponseInfo& getCollisionResponseInfo() const
    {
        return collision_response_info_;
    }
    CollisionResponseInfo& getCollisionResponseInfo()
    {
        return collision_response_info_;
    }

    bool hasBattery() const { return battery_ != nullptr; }

    powerlib::Battery *getBattery() { return battery_; }

    float getStateOfCharge() const
    {
        if (battery_ != nullptr) {
            return battery_->StateOfCharge();
        } else {
            return -100.0;
        }
    }

    float getVotage() const
    {
        if (battery_ != nullptr) {
            return battery_->Voltage();
        } else {
            return 0.0;
        }
    }

    float getNominalVoltage() const
    {
        if (battery_ != nullptr) {
            return battery_->NominalVoltage();
        } else {
            return 0.0;
        }
    }

    float getCapacity() const
    {
        if (battery_ != nullptr) {
            return battery_->Capacity();
        } else {
            return 0.0;
        }
    }

	double getDistanceTraveled() const
	{
		return distance_traveled_;
	}

	double getEnergyConsumed() const
	{
		return energy_consumed_;
	}

	double getTotalTime() const
	{
		return total_time_since_creation_;
	}


public:
    //for use in physics angine: //TODO: use getter/setter or friend method?
    TTimePoint last_kinematics_time;

private:
    real_T mass_, mass_inv_;
    Matrix3x3r inertia_, inertia_inv_;
	TTimeDelta total_time_since_creation_ = 0;
	Pose last_pose_; 
	double distance_traveled_ = -1;
	double distance_traveled_quanta_ = .1; //the smallest amount that would be accumulated to the distance traveled. This is set to cancel the accumulated error
	double energy_consumed_ = 0;


    Kinematics kinematics_;

    //force is in world frame but torque is not
    Wrench wrench_;

    CollisionInfo collision_info_;
    CollisionResponseInfo collision_response_info_;

    Environment* environment_ = nullptr;

protected:
    powerlib::Battery* battery_ = nullptr;
};

}} //namespace
#endif

